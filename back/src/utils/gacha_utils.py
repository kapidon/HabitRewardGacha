from typing import List

def parse_gacha_types(gacha_types_str: str) -> List[str]:
    """
    ガチャタイプの文字列を配列に変換します。

    Args:
        gacha_types_str (str): カンマ区切りのガチャタイプ文字列

    Returns:
        List[str]: 変換されたガチャタイプの配列
    """
    return [t.strip() for t in gacha_types_str.split(',')] 