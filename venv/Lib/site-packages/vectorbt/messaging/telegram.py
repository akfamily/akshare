# Copyright (c) 2021 Oleg Polakow. All rights reserved.
# This code is licensed under Apache 2.0 with Commons Clause license (see LICENSE.md for details)

"""Messaging using `python-telegram-bot`."""

import logging
from functools import wraps

from telegram import Update
from telegram.error import Unauthorized, ChatMigrated
from telegram.ext import (
    Handler,
    CallbackContext,
    Updater,
    Dispatcher,
    CommandHandler,
    MessageHandler,
    Filters,
    PicklePersistence,
    Defaults
)
from telegram.utils.helpers import effective_message_type

from vectorbt import _typing as tp
from vectorbt.utils.config import merge_dicts, get_func_kwargs, Configured
from vectorbt.utils.requests_ import text_to_giphy_url

logger = logging.getLogger(__name__)


class LogHandler(Handler):
    """Handler to log user updates."""

    def check_update(self, update: object) -> tp.Optional[tp.Union[bool, object]]:
        if isinstance(update, Update) and update.effective_message:
            message = update.effective_message
            message_type = effective_message_type(message)
            if message_type is not None:
                if message_type == 'text':
                    logger.info(f"{message.chat_id} - User: \"%s\"", message.text)
                else:
                    logger.info(f"{message.chat_id} - User: %s", message_type)
            return False
        return None


def send_action(action: str) -> tp.Callable:
    """Sends `action` while processing func command.

    Suitable only for bound callbacks taking arguments `self`, `update`, `context` and optionally other."""

    def decorator(func: tp.Callable) -> tp.Callable:
        @wraps(func)
        def command_func(self, update: Update, context: CallbackContext, *args, **kwargs) -> tp.Callable:
            if update.effective_chat:
                context.bot.send_chat_action(chat_id=update.effective_chat.id, action=action)
            return func(self, update, context, *args, **kwargs)

        return command_func

    return decorator


def self_decorator(self, func: tp.Callable) -> tp.Callable:
    """Pass bot object to func command."""

    def command_func(update, context, *args, **kwargs):
        return func(self, update, context, *args, **kwargs)

    return command_func


class TelegramBot(Configured):
    """Telegram bot.

    See [Extensions – Your first Bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot).

    `**kwargs` are passed to `telegram.ext.updater.Updater` and override
    settings under `messaging.telegram` in `vectorbt._settings.settings`.

    Usage:
        * Let's extend `TelegramBot` to track cryptocurrency prices:

        ```pycon
        >>> from telegram.ext import CommandHandler
        >>> import ccxt
        >>> import logging
        >>> import vectorbt as vbt

        >>> logging.basicConfig(level=logging.INFO)  # enable logging

        >>> class MyTelegramBot(vbt.TelegramBot):
        ...     @property
        ...     def custom_handlers(self):
        ...         return (CommandHandler('get', self.get),)
        ...
        ...     @property
        ...     def help_message(self):
        ...         return "Type /get [symbol] [exchange id (optional)] to get the latest price."
        ...
        ...     def get(self, update, context):
        ...         chat_id = update.effective_chat.id
        ...
        ...         if len(context.args) == 1:
        ...             symbol = context.args[0]
        ...             exchange = 'binance'
        ...         elif len(context.args) == 2:
        ...             symbol = context.args[0]
        ...             exchange = context.args[1]
        ...         else:
        ...             self.send_message(chat_id, "This command requires symbol and optionally exchange id.")
        ...             return
        ...         try:
        ...             ticker = getattr(ccxt, exchange)().fetchTicker(symbol)
        ...         except Exception as e:
        ...             self.send_message(chat_id, str(e))
        ...             return
        ...         self.send_message(chat_id, str(ticker['last']))

        >>> bot = MyTelegramBot(token='YOUR_TOKEN')
        >>> bot.start()
        INFO:vectorbt.utils.messaging:Initializing bot
        INFO:vectorbt.utils.messaging:Loaded chat ids [447924619]
        INFO:vectorbt.utils.messaging:Running bot vectorbt_bot
        INFO:apscheduler.scheduler:Scheduler started
        INFO:vectorbt.utils.messaging:447924619 - Bot: "I'm back online!"
        INFO:vectorbt.utils.messaging:447924619 - User: "/start"
        INFO:vectorbt.utils.messaging:447924619 - Bot: "Hello!"
        INFO:vectorbt.utils.messaging:447924619 - User: "/help"
        INFO:vectorbt.utils.messaging:447924619 - Bot: "Type /get [symbol] [exchange id (optional)] to get the latest price."
        INFO:vectorbt.utils.messaging:447924619 - User: "/get BTC/USDT"
        INFO:vectorbt.utils.messaging:447924619 - Bot: "55530.55"
        INFO:vectorbt.utils.messaging:447924619 - User: "/get BTC/USD bitmex"
        INFO:vectorbt.utils.messaging:447924619 - Bot: "55509.0"
        INFO:telegram.ext.updater:Received signal 2 (SIGINT), stopping...
        INFO:apscheduler.scheduler:Scheduler has been shut down
        ```
    """

    def __init__(self, giphy_kwargs: tp.KwargsLike = None, **kwargs) -> None:
        from vectorbt._settings import settings
        telegram_cfg = settings['messaging']['telegram']
        giphy_cfg = settings['messaging']['giphy']

        Configured.__init__(
            self,
            giphy_kwargs=giphy_kwargs,
            **kwargs
        )

        # Resolve kwargs
        giphy_kwargs = merge_dicts(giphy_cfg, giphy_kwargs)
        self.giphy_kwargs = giphy_kwargs
        default_kwargs = dict()
        passed_kwargs = dict()
        for k in get_func_kwargs(Updater.__init__):
            if k in telegram_cfg:
                default_kwargs[k] = telegram_cfg[k]
            if k in kwargs:
                passed_kwargs[k] = kwargs.pop(k)
        updater_kwargs = merge_dicts(default_kwargs, passed_kwargs)
        persistence = updater_kwargs.pop('persistence', None)
        if isinstance(persistence, str):
            persistence = PicklePersistence(persistence)
        defaults = updater_kwargs.pop('defaults', None)
        if isinstance(defaults, dict):
            defaults = Defaults(**defaults)

        # Create the (persistent) Updater and pass it your bot's token.
        logger.info("Initializing bot")
        self._updater = Updater(persistence=persistence, defaults=defaults, **updater_kwargs)

        # Get the dispatcher to register handlers
        self._dispatcher = self.updater.dispatcher

        # Register handlers
        self.dispatcher.add_handler(self.log_handler)
        self.dispatcher.add_handler(CommandHandler('start', self.start_callback))
        self.dispatcher.add_handler(CommandHandler("help", self.help_callback))
        for handler in self.custom_handlers:
            self.dispatcher.add_handler(handler)
        self.dispatcher.add_handler(MessageHandler(Filters.status_update.migrate, self.chat_migration_callback))
        self.dispatcher.add_handler(MessageHandler(Filters.command, self.unknown_callback))
        self.dispatcher.add_error_handler(self_decorator(self, self.__class__.error_callback))

        # Set up data
        if 'chat_ids' not in self.dispatcher.bot_data:
            self.dispatcher.bot_data['chat_ids'] = []
        else:
            logger.info("Loaded chat ids %s", str(self.dispatcher.bot_data['chat_ids']))

    @property
    def updater(self) -> Updater:
        """Updater."""
        return self._updater

    @property
    def dispatcher(self) -> Dispatcher:
        """Dispatcher."""
        return self._dispatcher

    @property
    def log_handler(self) -> LogHandler:
        """Log handler."""
        return LogHandler(lambda update, context: None)

    @property
    def custom_handlers(self) -> tp.Iterable[Handler]:
        """Custom handlers to add.

        Override to add custom handlers. Order counts."""
        return ()

    @property
    def chat_ids(self) -> tp.List[int]:
        """Chat ids that ever interacted with this bot.

        A chat id is added upon receiving the "/start" command."""
        return self.dispatcher.bot_data['chat_ids']

    def start(self, in_background: bool = False, **kwargs) -> None:
        """Start the bot.

        `**kwargs` are passed to `telegram.ext.updater.Updater.start_polling`
        and override settings under `messaging.telegram` in `vectorbt._settings.settings`."""
        from vectorbt._settings import settings
        telegram_cfg = settings['messaging']['telegram']

        # Resolve kwargs
        default_kwargs = dict()
        passed_kwargs = dict()
        for k in get_func_kwargs(self.updater.start_polling):
            if k in telegram_cfg:
                default_kwargs[k] = telegram_cfg[k]
            if k in kwargs:
                passed_kwargs[k] = kwargs.pop(k)
        polling_kwargs = merge_dicts(default_kwargs, passed_kwargs)

        # Start the Bot
        logger.info("Running bot %s", str(self.updater.bot.get_me().username))
        self.updater.start_polling(**polling_kwargs)
        self.started_callback()

        if not in_background:
            # Run the bot until you press Ctrl-C or the process receives SIGINT,
            # SIGTERM or SIGABRT. This should be used most of the time, since
            # start_polling() is non-blocking and will stop the bot gracefully.
            self.updater.idle()

    def started_callback(self) -> None:
        """Callback once the bot has been started.

        Override to execute custom commands upon starting the bot."""
        self.send_message_to_all("I'm back online!")

    def send(self, kind: str, chat_id: int, *args, log_msg: tp.Optional[str] = None, **kwargs) -> None:
        """Send message of any kind to `chat_id`."""
        try:
            getattr(self.updater.bot, 'send_' + kind)(chat_id, *args, **kwargs)
            if log_msg is None:
                log_msg = kind
            logger.info(f"{chat_id} - Bot: %s", log_msg)
        except ChatMigrated as e:
            # transfer data, if old data is still present
            new_id = e.new_chat_id
            if chat_id in self.chat_ids:
                self.chat_ids.remove(chat_id)
            self.chat_ids.append(new_id)
            # Resend to new chat id
            self.send(kind, new_id, *args, log_msg=log_msg, **kwargs)
        except Unauthorized as e:
            logger.info(f"{chat_id} - Unauthorized to send the %s", kind)

    def send_to_all(self, kind: str, *args, **kwargs) -> None:
        """Send message of any kind to all in `TelegramBot.chat_ids`."""
        for chat_id in self.chat_ids:
            self.send(kind, chat_id, *args, **kwargs)

    def send_message(self, chat_id: int, text: str, *args, **kwargs) -> None:
        """Send text message to `chat_id`."""
        log_msg = "\"%s\"" % text
        self.send('message', chat_id, text, *args, log_msg=log_msg, **kwargs)

    def send_message_to_all(self, text: str, *args, **kwargs) -> None:
        """Send text message to all in `TelegramBot.chat_ids`."""
        log_msg = "\"%s\"" % text
        self.send_to_all('message', text, *args, log_msg=log_msg, **kwargs)

    def send_giphy(self, chat_id: int, text: str, *args, giphy_kwargs: tp.KwargsLike = None, **kwargs) -> None:
        """Send GIPHY from text to `chat_id`."""
        if giphy_kwargs is None:
            giphy_kwargs = self.giphy_kwargs
        gif_url = text_to_giphy_url(text, **giphy_kwargs)
        log_msg = "\"%s\" as GIPHY %s" % (text, gif_url)
        self.send('animation', chat_id, gif_url, *args, log_msg=log_msg, **kwargs)

    def send_giphy_to_all(self, text: str, *args, giphy_kwargs: tp.KwargsLike = None, **kwargs) -> None:
        """Send GIPHY from text to all in `TelegramBot.chat_ids`."""
        if giphy_kwargs is None:
            giphy_kwargs = self.giphy_kwargs
        gif_url = text_to_giphy_url(text, **giphy_kwargs)
        log_msg = "\"%s\" as GIPHY %s" % (text, gif_url)
        self.send_to_all('animation', gif_url, *args, log_msg=log_msg, **kwargs)

    @property
    def start_message(self) -> str:
        """Message to be sent upon "/start" command.

        Override to define your own message."""
        return "Hello!"

    def start_callback(self, update: object, context: CallbackContext) -> None:
        """Start command callback."""
        if isinstance(update, Update) and update.effective_chat:
            chat_id = update.effective_chat.id
            if chat_id not in self.chat_ids:
                self.chat_ids.append(chat_id)
            self.send_message(chat_id, self.start_message)

    @property
    def help_message(self) -> str:
        """Message to be sent upon "/help" command.

        Override to define your own message."""
        return "Can't help you here, buddy."

    def help_callback(self, update: object, context: CallbackContext) -> None:
        """Help command callback."""
        if isinstance(update, Update) and update.effective_chat:
            chat_id = update.effective_chat.id
            self.send_message(chat_id, self.help_message)

    def chat_migration_callback(self, update: object, context: CallbackContext) -> None:
        """Chat migration callback."""
        if isinstance(update, Update) and update.message:
            old_id = update.message.migrate_from_chat_id or update.message.chat_id
            new_id = update.message.migrate_to_chat_id or update.message.chat_id
            if old_id in self.chat_ids:
                self.chat_ids.remove(old_id)
            self.chat_ids.append(new_id)
            logger.info(f"{old_id} - Chat migrated to {new_id}")

    def unknown_callback(self, update: object, context: CallbackContext) -> None:
        """Unknown command callback."""
        if isinstance(update, Update) and update.effective_chat:
            chat_id = update.effective_chat.id
            logger.info(f"{chat_id} - Unknown command \"{update.message}\"")
            self.send_message(chat_id, "Sorry, I didn't understand that command.")

    def error_callback(self, update: object, context: CallbackContext, *args) -> None:
        """Error callback."""
        logger.error("Exception while handling an update \"%s\": ", update, exc_info=context.error)
        if isinstance(update, Update) and update.effective_chat:
            chat_id = update.effective_chat.id
            self.send_message(chat_id, "Sorry, an error happened.")

    def stop(self) -> None:
        """Stop the bot."""
        logger.info("Stopping bot")
        self.updater.stop()

    @property
    def running(self) -> bool:
        """Whether the bot is running."""
        return self.updater.running
