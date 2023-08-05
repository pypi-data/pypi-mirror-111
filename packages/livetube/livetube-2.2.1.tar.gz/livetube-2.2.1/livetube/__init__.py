"""
    livetube - A API for youtube streaming
    作者: Sam
    创建日期: 2020/12/18 10:18
    文件:    __init__.py
    文件描述:
    Extra note: All check passed. Not even a warning
"""
__title__ = "livetube"
__author__ = "Sam"

import asyncio

try:
    # noinspection PyUnresolvedReferences
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ModuleNotFoundError:
    pass

from livetube.__main__ import Video, Membership, Community, Studio
from livetube.util.exceptions import *

__all__ = [
    # Objects
    "Video", "Membership", "Community", "Studio",
    # Base error
    "LivetubeError", "ExtractError",
    # Errors
    "NetworkError", "HTMLParseError", "RegexMatchError", "LiveStreamOffline",
    "VideoUnavailable", "PaymentRequired", "VideoPrivate", "RecordingUnavailable",
    "MembersOnly", "LoginRequired", "AccountBanned", "VideoRegionBlocked"
]
