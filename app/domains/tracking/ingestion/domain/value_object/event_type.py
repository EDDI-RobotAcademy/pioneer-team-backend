from enum import Enum


class EventType(str, Enum):
    LAND = "LAND"
    IMPRESSION = "IMPRESSION"
    START = "START"
    CONVERT = "CONVERT"
    SHARE = "SHARE"
