from __future__ import annotations

from typing import Any


def normalize_jpx_ticker(code: Any) -> str | None:
    if code is None:
        return None

    code_str = str(code).strip().upper()
    if not code_str or code_str in {"NAN", "NONE"}:
        return None

    if code_str.endswith(".0"):
        code_str = code_str[:-2]

    code_str = code_str.replace("　", "").replace(" ", "")

    if len(code_str) == 5 and code_str.endswith("0"):
        if code_str[-2].isalpha() or code_str[:-1].isdigit():
            code_str = code_str[:-1]

    if code_str.isdigit() and len(code_str) < 4:
        code_str = code_str.zfill(4)

    if not code_str:
        return None

    return f"{code_str}.T"
