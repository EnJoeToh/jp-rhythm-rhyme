import pytest
import json
import jatext_utils as jt
from kana_text import KanaText

def test_kanaized_text():
    assert jt.plain_text_to_kanaized_text("「日本語」") == "「にほんご」"
    assert jt.plain_text_to_kanaized_text("　ぜんかく はんかく") == "　ぜんかく はんかく"
    assert jt.plain_text_to_kanaized_text("2025") == "2025"
    assert jt.plain_text_to_kanaized_text("２０２５") == "２０２５"
    assert jt.plain_text_to_kanaized_text("二千二十五") == "にせんにじゅうご"
    assert jt.plain_text_to_kanaized_text("コンピューターだよ") == "コンピューターだよ"
    assert jt.plain_text_to_kanaized_text("こんぴゅーたーだよ") == "こんぴゅーたーだよ"

with open("cv_map.json", "r", encoding="utf-8") as f:
        cv_map = json.load(f)

@pytest.mark.parametrize("text, moras_expected, vowels_expected", [
    ("かぉ", ["か", "ぉ"], ["a", "ぉ"]),
    ("かわ", ["か","わ"], ["a","a"]),
    ("ティー", ["てぃ","い"], ["i","i"]),
    ("そうかぁと", ["そ", "う", "か", "ぁ", "と"], ["o", "u", "a", "ぁ", "o"]),
    ("リィ", ["り", "ぃ"], ["i", "ぃ"]),
    ("だよ", ["だ", "よ"], ["a", "o"]),
    ("フィレオフィッシュ", ["ふぃ", "れ", "お", "ふぃ", "っ", "しゅ"], ["i", "e", "o", "i", "っ", "u"]),
    ("ツァトゥグア", ["つぁ", "とぅ", "ぐ", "あ"], ["a", "u", "u", "a"])
])
def test_mora_and_vowels(text, moras_expected, vowels_expected):
    kt = KanaText(text, cv_map)
    assert kt.moras() == moras_expected
    assert kt.vowels() == vowels_expected
