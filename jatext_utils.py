import pykakasi

restricted_hiragana_set = {
"あ", "い", "う", "え", "お",
"か", "き", "く", "け", "こ",
"さ", "し", "す", "せ", "そ",
"た", "ち", "つ", "て", "と",
"な", "に", "ぬ", "ね", "の",
"は", "ひ", "ふ", "へ", "ほ",
"ま", "み", "む", "め", "も",
"や", "ゆ", "よ",
"わ", "ゐ", "ゑ", "を",
"っ", "ゔ", "ん",
"が", "ぎ", "ぐ", "げ", "ご",
"ざ", "じ", "ず", "ぜ", "ぞ",
"だ", "じ", "づ", "で", "ど",
"ば", "び", "ぶ", "べ", "ぼ",
"ぱ", "ぴ", "ぷ", "ぺ", "ぽ",
"ぁ", "ぃ", "ぅ", "ぇ", "ぉ",
"ゃ", "ゅ", "ょ",
"ゎ", "ゕ", "ゖ"}

def hiragana_to_katakana(s: str) -> str:
    out = []
    for ch in s:
        if 0x3041 <= ord(ch) <= 0x3096:
            out.append(chr(ord(ch) + 0x60))
        else:
            out.append(ch)
    return "".join(out) 

def katakana_to_hiragana(s :str) -> str:
    out = []
    for ch in s:
        if 0x30A1 <= ord(ch) <= 0x30F6:
            out.append(chr(ord(ch) - 0x60))
        else:
            out.append(ch)
    return "".join(out) 

restricted_katakana_set = {hiragana_to_katakana(ch) for ch in restricted_hiragana_set}

restricted_kigou_set = {"ー"}

restricted_kana_set = restricted_hiragana_set | restricted_katakana_set | restricted_kigou_set

restricted_hiragana_small_set = {"ぁぃぅぇぉゃゅょゎっゕゖ"}
restricted_hiragana_large_set = restricted_hiragana_set - restricted_hiragana_small_set

SMALLS = set("ぁぃぅぇぉゃゅょ")
SOKUON = "っ"
CHOON = "ー"
HATSUON = "ん"

def plain_text_to_kanaized_text(s: str) -> str:
    """
    漢字とひらがなはひらがな化、カタカナはそのまま残す。
    エスケープ文字はややこしいので突っ込まないこと。
    """
    kks = pykakasi.kakasi()
    result = kks.convert(s)
    
    out = []
    for item in result:
        o   = item["orig"]
        hira = item.get("hira", "")
        kana = item.get("kana", "")

        if o == kana:                 # カタカナはそのまま
            out.append(o)
        elif hira:                     # ひらがな or 漢字（読みが取れたら hira が入る）
            out.append(hira)
        else:                          # それ以外（英数記号・空白・絵文字・改行 等）
            out.append(o)

    return "".join(out)
