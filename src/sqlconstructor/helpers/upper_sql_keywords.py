# coding=utf-8
"""
Module for helpers to upper sql keywords
"""

__author__ = 'https://github.com/akvilary'

import re
from typing import Tuple


def upper_keywords(text: str, keywords: Tuple[str]) -> str:
    """Upper certain keywords in string (case insensitive)"""
    for keyword in keywords:
        if keyword.lower() in text.lower():
            pattern = (
                r'(--.*?\Z)|(\/\*[\s\S]*?\*\/)|(".*?")|(\'.*?\')|'
                r'\b' + keyword + r'\b'
            )
            text = re.sub(
                pattern,
                upper_keyword_if_required,
                text,
                flags=re.I,
            )
    return text


def upper_keyword_if_required(match):
    """
    Upper keyword if keyword:
    1) Located not in inline sql comment
    2) Located not in multiline sql comment
    3) Located not between single quotes
    4) Located not between double quotes
    """
    groups = match.groups()
    if any(groups):
        return match.group()
    return match.group().upper()
