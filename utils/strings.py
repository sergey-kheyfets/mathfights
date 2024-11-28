from __future__ import annotations
from typing import TypeGuard

import re


def sanitize_string(raw_str: str | None) -> str:
    if not raw_str:
        return ""
    return raw_str.strip().replace('"', "_")

def try_extract_number_as_str(num_str: str, default_str: str = "0") -> str:
    search_result = re.search(r"\d+", num_str)
    if not search_result:
        return default_str
    return search_result.group()
