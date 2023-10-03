import pytest
from src.scraper import camel_case_split


def test_camel_case_split1():
    result = camel_case_split("ThisIs anExample")
    assert result == "This Is an Example"


def test_camel_case_split2():
    result = camel_case_split("ThisIs anExample**disclaimer")
    assert result == "This Is an Example**disclaimer"
