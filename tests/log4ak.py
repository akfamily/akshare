import logging
import os
from logging.handlers import RotatingFileHandler


class LevelFilter(logging.Filter):
    """精准级别过滤器[1,4](@ref)"""
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

class LogManager:
    def __init__(self, log_dir="log", log_level=logging.DEBUG):
        """支持动态日志级别配置[5,8](@ref)"""
        # 目录结构初始化
        self.log_dir = log_dir
        self._init_log_dirs(log_dir)
        
        # 主记录器配置
        self.logger = logging.getLogger("SmartLogger")
        self.logger.setLevel(log_level)  # 动态设置主日志级别

        # 清除已有处理器
        if hasattr(self, '_is_initialized'):  # 防止重复初始化
            return
        self.logger.handlers.clear()
        
        self._setup_handlers(log_level)
        self._is_initialized = True  # 标记初始化状态
    
    def _init_log_dirs(self, log_dir):
        """创建多级日志目录[3](@ref)"""
        os.makedirs(os.path.join(log_dir, "debug"), exist_ok=True)
        os.makedirs(os.path.join(log_dir, "info"), exist_ok=True)
        os.makedirs(os.path.join(log_dir, "error"), exist_ok=True)

    def _setup_handlers(self, log_level):
        # 关键修改2：重构处理器逻辑
        handlers = [
            self._create_debug_handler(),
            self._create_info_handler(),
            self._create_error_handler(),
            self._create_console_handler(log_level)
        ]
        
        # 关键修改3：统一添加处理器
        for handler in handlers:
            self.logger.addHandler(handler)

    def _create_debug_handler(self):
        handler = self._create_file_handler("debug/debug.log", logging.DEBUG)
        # 关键修改4：添加反向过滤器
        handler.addFilter(lambda r: r.levelno == logging.DEBUG)
        return handler

    def _create_info_handler(self):
        handler = self._create_file_handler("info/info.log", logging.INFO)
        handler.addFilter(lambda r: r.levelno >= logging.INFO)
        return handler

    def _create_error_handler(self):
        handler = self._create_file_handler("error/error.log", logging.ERROR)
        handler.addFilter(lambda r: r.levelno >= logging.ERROR)  # 包含ERROR及以上
        return handler

    def _create_console_handler(self, log_level):
        handler = logging.StreamHandler()
        # 关键修改5：动态控制台级别
        handler.setLevel(max(log_level, logging.ERROR))
        handler.setFormatter(self._create_formatter())
        # 关键修改6：排除文件已处理的级别
        handler.addFilter(lambda r: r.levelno >= logging.ERROR and 
                         r.levelno not in [logging.DEBUG, logging.INFO])
        return handler

    def _create_formatter(self):
        """统一日志格式[7](@ref)"""
        return logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def _create_file_handler(self, rel_path, level):
        """创建轮转文件处理器[2,8](@ref)"""
        handler = RotatingFileHandler(
            filename=os.path.join(self.log_dir, rel_path),
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        handler.setLevel(level)
        handler.addFilter(LevelFilter(level))
        handler.setFormatter(self._create_formatter())
        return handler

    def _create_console_handler(self, level):
        """创建控制台处理器[7](@ref)"""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(self._create_formatter())
        return console_handler

    # 保留原有接口方法
    def debug(self, msg): self.logger.debug(msg)
    def info(self, msg): self.logger.info(msg) 
    def error(self, msg): self.logger.error(msg)



# 使用示例
if __name__ == "__main__":
        

    # DEBUG模式（文件记录,控制台显示DEBUG，INFO，ERROR）
    log = LogManager(log_level=logging.DEBUG)
    log.debug("用户登录参数校验通过")  
    log.info("获取用户参数")          
    log.error("数据库连接失败")      

    # INFO模式（文件记录,控制台显示INFO，ERROR）
    info_log = LogManager(log_level=logging.INFO)
    info_log.debug("调用接口")       
    info_log.info("成功记录")        
    info_log.error("服务不可用")    
    

    # ERROR模式（文件记录,控制台显示ERROR）
    err_log = LogManager(log_level=logging.ERROR)
    err_log.debug("调试信息")       
    err_log.info("返回参数信息")    
    err_log.error("参数类型错误")    
