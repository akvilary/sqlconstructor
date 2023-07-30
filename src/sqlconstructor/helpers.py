# coding=utf-8
"""Helpers which are used in multiple modules"""

__author__ = 'https://github.com/akvilary'

import re
from typing import Tuple

def indent_lines(text: str, ind: int) -> str:
    """Indent each line of the string"""
    text = ''.join((' ' * ind) + x + '\n' for x in text.splitlines()).rstrip()
    return text


def upper_keywords(text: str, keywords: Tuple[str]) -> str:
    """Upper certain keywords in string (case insensitive)"""
    for keyword in keywords:
        if keyword.lower() in text.lower():
            pattern = r'\b' + keyword + r'\b'
            text = re.sub(
                pattern,
                keyword.upper(),
                text,
                flags=re.IGNORECASE,
            )
    return text
