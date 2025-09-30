import json
from jatext_utils import plain_text_to_kanaized_text
from kana_text import KanaText

# cv_map.json を読む
with open("cv_map.json", "r", encoding="utf-8") as f:
    cv_map = json.load(f)

def vowerl_viewer_on_CLI(ss: str) -> str:
    for s in ss.split("\n"):
        kt = KanaText(s, cv_map)
        moras = kt.moras()
        vowels = kt.vowels()
        top, bottom = align_mora_vowel_lines(moras, vowels)
        print(top); print(bottom); print("\n")

FWSPACE = "　"  # 全角スペース
TABLE = str.maketrans("aiueoN", "ＡＩＵＥＯＮ")  # 母音を全角大文字に

def align_mora_vowel_lines(moras: list[str], vowels: list[str]) -> tuple[str, str]:
    top_parts = []
    bot_parts = []
    for m, v in zip(moras, vowels):
        top_parts.append(m)
        # モーラの見かけ幅＝コードポイント数でOK（例: "ふぁ"→2）
        pad = FWSPACE * (len(m) - 1)
        bot_parts.append(v.translate(TABLE) + pad)
    return "".join(top_parts), "".join(bot_parts)


text0 = "今日はティーを飲む"
kanaized = plain_text_to_kanaized_text(text0)
kanaized_text0 = "きょうはティーをのむ"

kanaized_text1 = "かぜをおて　　　ひそかにひらく　　はうひのこうを　　　またず\nはるをむかへて　たちまちにへんず　まさにうろのおんを　ねがはむとす"

kanaized_text2 = "としのうちに\nはるはきにけり\nひととせを\nこぞとやいはむ\nことしとやいはむ"
kanaized_text3 = plain_text_to_kanaized_text("ふんぐるい　むぐるうなふ　くとぅぐあ　ふぉまるはうと　んがあ・ぐあ　なふるたぐん　いあ！　くとぅぐあ！")
kanaized_text4 = plain_text_to_kanaized_text("シャアのシャツをシャットアウト")

vowerl_viewer_on_CLI(kanaized_text0)
vowerl_viewer_on_CLI(kanaized_text1)
vowerl_viewer_on_CLI(kanaized_text2)
vowerl_viewer_on_CLI(kanaized_text3)
vowerl_viewer_on_CLI(kanaized_text4)



