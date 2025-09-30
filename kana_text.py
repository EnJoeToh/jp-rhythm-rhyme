# kana_text.py
from typing import Dict, List, Tuple
import jatext_utils as jt

restricted_hiragana_set = jt.restricted_hiragana_set

SMALLS = jt.SMALLS
SOKUON = jt.SOKUON
CHOON = jt.CHOON
HATSUON = jt.HATSUON

class KanaText:
    """
    仕様：
      - コンストラクタは *人力で修正済み* kanaized テキスト（ひらがな＋カタカナ＋記号）を受け取る。
      - raw() はその文字列をそのまま返す。
      - moras() は以下の規則でモーラ配列を返す：
          1) 一旦テキスト全体をひらがな化
          2) restricted_hiragana_set に無い文字は素通し（1文字が1モーラ相当の“非かなトークン”）
          3) 「っ」は単独モーラ
          4) 「っ」以外の小書き(ゃゅょぁぃぅぇぉ)は、直前が“大きなひらがな”なら直前に結合、そうではないならそのまま単独
          5) ー は直前にモーラがあり、かつ cv_map で V が引けて _v2kana があるなら、その母音かなを追加
          それ以外は ー を素通し
    """
    def __init__(self, kanaized_text: str, cv_map: Dict[str, Dict[str, str]]):
        self._kanaized_text = kanaized_text
        self._cv_map = cv_map

        # is_vowel=true のエントリを母音逆引きに使う: Vコード -> ひらがな
        # 例: {"a":"あ","i":"い","u":"う","e":"え","o":"お","ん":"ん","っ":"っ"}
        self._v2kana: Dict[str, str] = {
            entry["V"]: kana
            for kana, entry in cv_map.items()
            if entry.get("is_vowel") is True and isinstance(entry.get("V"), str)
        }

    def text(self) -> str:
        """入力として渡された kanaized_text_text をそのまま返す。"""
        return self._kanaized_text
    
    def moras(self) -> List[str]:
        h = jt.katakana_to_hiragana(self._kanaized_text)
        moras: List[str] = []
        for ch in h:
            # 非かなは素通し（そのまま1トークンとして置く）
            if not (ch in jt.restricted_hiragana_set) and ch != CHOON:
                moras.append(ch)
                continue

            # 促音
            if ch == SOKUON:
                moras.append(SOKUON)
                continue

            # 長音
            if ch == CHOON:
                if moras:
                    prev = moras[-1]
                    prev_entry = self._cv_map.get(prev)
                    if prev_entry is not None:
                        vcode = prev_entry.get("V")
                        vkana = self._v2kana.get(vcode)
                        if vkana:
                            moras.append(vkana)   # 例: "カー" -> ["か","あ"]
                            continue
                moras.append(CHOON)              # 先頭/未登録/逆引不可 → 素通し
                continue

            # 小書き：cv_map に「直前 + 小書き」がキーとして存在するときだけ結合
            if ch in SMALLS:
                if moras and (moras[-1] + ch) in self._cv_map:
                    moras[-1] = moras[-1] + ch         # 例: "ふ"+"ぁ" -> "ふぁ"（ファ）
                else:
                    moras.append(ch)                 # 例: "か" の後の "ぁ" は独立（そうかぁ）
                continue

            # 通常の“大きなひらがな”
            moras.append(ch)

        return moras
    
    def syllables(self) -> List[str]:
        pass

    def cv_pairs(self) -> List[tuple[str, str]]:
        """モーラ列から (C,V) のペアを返す"""
        pairs = []
        for m in self.moras():
            entry = self._cv_map.get(m)
            if entry:
                pairs.append((entry["C"], entry["V"]))
            else:
                # 辞書にない場合は素通し
                pairs.append((m, m))
        return pairs

    def vowels(self) -> List[str]:
        """母音列"""
        return [v for _, v in self.cv_pairs()]

    def consonants(self) -> List[str]:
        """子音列"""
        return [c for c, _ in self.cv_pairs()]