# -*- coding: utf-8 -*-
"""
Date: 2026/05/02
Desc: TapTap 游戏榜单数据接口
"""
import re
import time
from typing import Optional

import pandas as pd
import requests


# ============================================================
# 常量配置
# ============================================================
_TAPTAP_BASE_URL = "https://www.taptap.cn/webapiv2/app-top/v2/hits"

_TAPTAP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/18.0 Mobile/15E148 Safari/604.1"
    ),
    "Referer": "https://www.taptap.cn/",
    "Accept": "application/json, text/plain, */*",
}

_TAPTAP_X_UA = (
    "V=1&PN=WebM&LANG=zh_CN&VN_CODE=102&LOC=CN&PLT=iOS&DS=Android"
    "&UID=12f0a48b-bd25-4dce-9d50-27924e83da1d&OS=iOS&OSV=18.5"
)

# 内部参数（不对外暴露）
_TAPTAP_TIMEOUT = 15.0
_TAPTAP_SLEEP = 0.4
_TAPTAP_PAGE_SIZE = 10
_TAPTAP_MAX_LOOPS = 200

# 榜单类型枚举
_TAPTAP_RANK_TYPE_MAP = {
    "热玩榜": "pop",
    "热门榜": "hot",
    "新品榜": "new",
    "预约榜": "reserve",
    "热卖榜": "sell",
}


def _clean_html(text: Optional[str]) -> str:
    """清洗 HTML 标签和实体字符"""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    text = str(text)
    text = re.sub(r"<br[^>]*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    replacements = {
        "&amp;": "&", "&lt;": "<", "&gt;": ">",
        "&#34;": '"', "&#39;": "'", "&quot;": '"', "&nbsp;": " ",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def game_hot_rank_taptap(symbol: str = "热玩榜") -> pd.DataFrame:
    """
    TapTap-游戏榜单
    https://www.taptap.cn/top/played

    :param symbol: 榜单类型; 可选 {"热玩榜", "热门榜", "新品榜", "预约榜", "热卖榜"}
    :type symbol: str
    :return: 游戏榜单数据
    :rtype: pandas.DataFrame
    """
    if symbol not in _TAPTAP_RANK_TYPE_MAP:
        raise ValueError(
            f"symbol 仅支持 {list(_TAPTAP_RANK_TYPE_MAP.keys())}, 当前传入: {symbol}"
        )
    type_name = _TAPTAP_RANK_TYPE_MAP[symbol]
    session = requests.Session()
    session.headers.update(_TAPTAP_HEADERS)
    all_games = []
    total: Optional[int] = None
    offset = 0
    for _ in range(_TAPTAP_MAX_LOOPS):
        params = {
            "from": offset,
            "limit": _TAPTAP_PAGE_SIZE,
            "type_name": type_name,
            "X-UA": _TAPTAP_X_UA,
        }
        r = session.get(_TAPTAP_BASE_URL, params=params, timeout=_TAPTAP_TIMEOUT)
        r.raise_for_status()
        js = r.json()
        if not js.get("success"):
            raise RuntimeError(f"TapTap 接口返回失败: {js}")
        data = js.get("data", {}) or {}
        page_list = data.get("list", []) or []
        if total is None:
            total = data.get("total", 0)
        if not page_list:
            break
        all_games.extend(page_list)
        if total and len(all_games) >= total:
            break
        offset += _TAPTAP_PAGE_SIZE
        time.sleep(_TAPTAP_SLEEP)
    if not all_games:
        return pd.DataFrame()
    df = pd.json_normalize(all_games)
    df["标签"] = [
        ", ".join([t.get("value", "") for t in (item.get("app", {}).get("tags") or [])])
        for item in all_games
    ]
    rename_map = {
        "app.id": "游戏ID",
        "app.title": "游戏名称",
        "app.icon.url": "图标链接",
        "app.stat.rating.score": "评分",
        "app.stat.hits_total": "总点击量",
        "app.stat.play_total": "游玩次数",
        "app.stat.review_count": "评论数",
        "app.stat.fans_count": "粉丝数",
        "app.description.text": "简介",
        "app.rec_text": "推荐语",
        "app.released_time": "发布时间戳",
    }
    df.rename(columns=rename_map, inplace=True)
    if "评分" in df.columns:
        df["评分"] = pd.to_numeric(df["评分"], errors="coerce").astype("float64")
    for col in ["总点击量", "游玩次数", "评论数", "粉丝数"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    if "发布时间戳" in df.columns:
        df["发布时间"] = pd.to_datetime(
            df["发布时间戳"], unit="s", errors="coerce"
        )
    for col in ["游戏名称", "游戏ID", "图标链接", "推荐语", "标签"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()
    if "简介" in df.columns:
        df["简介"] = df["简介"].apply(_clean_html).astype("string")

    columns_order = [
        "游戏名称", "评分", "总点击量", "游玩次数", "评论数",
        "粉丝数", "标签", "推荐语", "发布时间",
        "游戏ID", "图标链接", "简介",
    ]
    df = df[[c for c in columns_order if c in df.columns]]
    df = df.drop_duplicates(subset=["游戏ID"]).reset_index(drop=True)
    df.insert(0, "排名", df.index + 1)
    return df


if __name__ == "__main__":
    game_hot_rank_taptap_df = game_hot_rank_taptap(symbol="热玩榜")
    print(game_hot_rank_taptap_df)

    game_hot_rank_taptap_df = game_hot_rank_taptap(symbol="热门榜")
    print(game_hot_rank_taptap_df)

    game_hot_rank_taptap_df = game_hot_rank_taptap(symbol="新品榜")
    print(game_hot_rank_taptap_df)

    game_hot_rank_taptap_df = game_hot_rank_taptap(symbol="预约榜")
    print(game_hot_rank_taptap_df)

    game_hot_rank_taptap_df = game_hot_rank_taptap(symbol="热卖榜")
    print(game_hot_rank_taptap_df)
