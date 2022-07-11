# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/3/18 19:45
Desc: 缓存工具
"""
from datetime import timedelta
from requests_cache import CachedSession

session = CachedSession(
    'ak_cache',
    use_temp=True,
    # use_cache_dir=True,                # Save files in the default user cache dir
    cache_control=False,                # Use Cache-Control headers for expiration, if available
    expire_after=timedelta(days=1),    # Otherwise expire responses after one day
    allowable_methods=['GET', 'POST'],  # Cache POST requests to avoid sending the same data twice
    allowable_codes=[200],        # Cache 400 responses as a solemn reminder of your failures
    ignored_parameters=['api_key'],    # Don't match this param or save it in the cache
    match_headers=False,                # Match all request headers
    stale_if_error=False,               # In case of request errors, use stale cache data if possible
)
