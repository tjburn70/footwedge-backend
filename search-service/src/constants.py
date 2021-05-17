from enum import Enum


class QueryType(str, Enum):
    MATCH = "match"
    MULTI_MATCH = "multi_match"
    WILDCARD = "wildcard"
