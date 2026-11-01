#!/usr/bin/env python3
"""Amigurumi 구조화 도안(JSON) 검증기.

output-spec.md 3장의 검증 규칙 V1~V8을 검사합니다.

사용법:
    python validate_pattern.py examples/chick.pattern.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).with_name("pattern.schema.json")

# op -> (쓰는 코, 만드는 코) : 1회 기준
STITCH_MATH = {
    "sc": (1, 1),
    "hdc": (1, 1),
    "dc": (1, 1),
    "sl_st": (1, 1),
    "inc": (1, 2),
    "dec": (2, 1),
    "ch": (0, 1),
    "skip": (1, 0),
    "color": (0, 0),
}


def count_stitches(stitches: list[dict]) -> tuple[int, int, bool]:
    """(쓰는 코 합, 만드는 코 합, 늘림/줄임 포함 여부)를 계산합니다."""
    consumed = produced = 0
    shaping = False
    for st in stitches:
        op = st["op"]
        if op == "repeat":
            c, p, s = count_stitches(st["body"])
            consumed += c * st["times"]
            produced += p * st["times"]
            shaping |= s
            continue
        n = 0 if op == "color" else st.get("n", 1)
        c, p = STITCH_MATH[op]
        consumed += c * n
        produced += p * n
        shaping |= op in ("inc", "dec")
    return consumed, produced, shaping


def validate(pattern: dict) -> list[str]:
    errors: list[str] = []

    # V1 스키마
    try:
        import jsonschema
    except ImportError:
        print("[warn] jsonschema가 설치되어 있지 않아 V1(스키마) 검사를 건너뜁니다. (pip install jsonschema)")
    else:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        for err in sorted(validator.iter_errors(pattern), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in err.path) or "(root)"
            errors.append(f"V1 스키마: {loc}: {err.message}")
        if errors:
            return errors  # 구조가 깨졌으면 이후 검사는 의미 없음

    yarn_ids = {y["id"] for y in pattern["materials"]["yarns"]}
    parts = {p["id"]: p for p in pattern["parts"]}

    for part in pattern["parts"]:
        pid = part["id"]
        rounds = part["rounds"]

        # V6 실 참조
        if part["yarn"] not in yarn_ids:
            errors.append(f"V6 참조: {pid}: 존재하지 않는 실 '{part['yarn']}'")

        expected_from = 1
        prev_count = None
        for rnd in rounds:
            label = f"{pid} R{rnd['from']}" + (f"–R{rnd['to']}" if rnd["to"] != rnd["from"] else "")

            # V2 단 연속성
            if rnd["from"] != expected_from or rnd["to"] < rnd["from"]:
                errors.append(f"V2 단 연속성: {label}: R{expected_from}부터 시작해야 합니다")
            expected_from = rnd["to"] + 1

            consumed, produced, shaping = count_stitches(rnd["stitches"])
            first = rnd["from"] == 1

            # V3 코 사용 일치
            if first:
                if part["start"]["type"] == "magic_ring" and produced != part["start"]["count"]:
                    errors.append(f"V3 코 사용: {label}: 매직링 {part['start']['count']}코인데 {produced}코를 뜹니다")
            elif consumed != prev_count:
                errors.append(f"V3 코 사용: {label}: 이전 단 {prev_count}코인데 {consumed}코를 사용합니다")

            # V4 코 수 일치
            if produced != rnd["count"]:
                errors.append(f"V4 코 수: {label}: 계산 결과 {produced}코인데 count={rnd['count']}")

            # V5 범위 단
            if rnd["to"] > rnd["from"] and (shaping or consumed != produced):
                errors.append(f"V5 범위 단: {label}: 여러 단을 묶은 단에서는 코 수가 변하면 안 됩니다")

            # V6 색 바꾸기 실 참조
            for st in _walk(rnd["stitches"]):
                if st["op"] == "color" and st["yarn"] not in yarn_ids:
                    errors.append(f"V6 참조: {label}: 존재하지 않는 실 '{st['yarn']}'")

            prev_count = rnd["count"]

        # V7 순서 제약 (닫는 파츠는 마지막 단 이후 더 이상 작업 불가)
        actions = [a["type"] for r in rounds for a in r.get("actions", [])]
        if part["stuffing"] != "none" and part["finish"]["type"] == "close" and "stuff" not in actions:
            errors.append(f"V7 순서: {pid}: 솜을 넣는 파츠인데 닫기 전에 'stuff' 작업이 없습니다")
        last_round = rounds[-1]["to"]
        for r in rounds:
            for a in r.get("actions", []):
                if a["type"] == "insert_safety_eyes" and part["finish"]["type"] == "close" and r["to"] >= last_round:
                    errors.append(f"V7 순서: {pid}: 안전눈은 마지막 단보다 먼저 끼워야 합니다")
                if "between_rounds" in a and max(a["between_rounds"]) > last_round:
                    errors.append(f"V8 위치: {pid}: 안전눈 위치 {a['between_rounds']}가 단 범위를 벗어납니다")

    # V6 / V8 조립·디테일 참조와 위치
    for kind, items in (("assembly", pattern.get("assembly", [])), ("details", pattern.get("details", []))):
        for i, item in enumerate(items):
            tag = f"{kind}[{i}]"
            if kind == "assembly" and item["part"] not in parts:
                errors.append(f"V6 참조: {tag}: 존재하지 않는 파츠 '{item['part']}'")
            if item.get("yarn") and item["yarn"] not in yarn_ids:
                errors.append(f"V6 참조: {tag}: 존재하지 않는 실 '{item['yarn']}'")
            target = parts.get(item["target"])
            if target is None:
                errors.append(f"V6 참조: {tag}: 존재하지 않는 대상 파츠 '{item['target']}'")
                continue
            pos = item.get("position")
            if pos:
                lo, hi = pos["rounds"]
                if lo > hi or lo < 1 or hi > target["rounds"][-1]["to"]:
                    errors.append(f"V8 위치: {tag}: 단 범위 {pos['rounds']}가 '{target['id']}'의 단 범위를 벗어납니다")

    return errors


def _walk(stitches: list[dict]):
    for st in stitches:
        yield st
        if st["op"] == "repeat":
            yield from _walk(st["body"])


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    pattern = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    errors = validate(pattern)
    if errors:
        print(f"❌ {len(errors)}개 오류")
        for e in errors:
            print(f"  - {e}")
        return 1
    total_rounds = sum(p["rounds"][-1]["to"] for p in pattern["parts"])
    print(f"✅ 유효한 도안: {pattern['meta']['title']} (파츠 {len(pattern['parts'])}개, 총 {total_rounds}단)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
