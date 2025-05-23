default_parsers = [
    "timestamp",
    "relative-time",
    "custom-formats",
    "absolute-time",
]

settings = {
    # Date order
    "DATE_ORDER": "MDY",
    "PREFER_LOCALE_DATE_ORDER": True,
    # Timezone related
    "TIMEZONE": "local",
    "TO_TIMEZONE": False,
    "RETURN_AS_TIMEZONE_AWARE": "default",
    # Incomplete dates
    "PREFER_DAY_OF_MONTH": "current",
    "PREFER_MONTH_OF_YEAR": "current",
    "PREFER_DATES_FROM": "current_period",
    "RELATIVE_BASE": False,
    "STRICT_PARSING": False,
    "REQUIRE_PARTS": [],
    # Language detection
    "SKIP_TOKENS": ["t"],
    "NORMALIZE": True,
    "DEFAULT_LANGUAGES": [],
    # Optional language detection
    "LANGUAGE_DETECTION_CONFIDENCE_THRESHOLD": 0.5,
    # Other settings
    "RETURN_TIME_AS_PERIOD": False,
    "PARSERS": default_parsers,
    "CACHE_SIZE_LIMIT": 1000,
}
