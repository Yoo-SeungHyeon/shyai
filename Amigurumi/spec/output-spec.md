# Amigurumi Output 정의서 (v0.1)

Amigurumi 모델이 **무엇을 출력해야 하는지** 정의하는 문서입니다.
모델 버전(`v0.1/`, `v0.2/` …)이 바뀌어도 이 출력 규격을 기준으로 결과물을 만들고 평가합니다.

---

## 1. 실제 아미구루미 도안의 구성

시중 아미구루미 도안(PDF, 블로그, 서적)은 대부분 아래 순서로 구성됩니다.

| 순서 | 섹션 | 내용 |
| --- | --- | --- |
| 1 | 개요 | 작품 이름, 완성 사진, 완성 크기, 난이도 |
| 2 | 재료 및 도구 | 실(색상·굵기·사용량), 코바늘 호수, 안전눈, 솜, 단수표시핀, 돗바늘 |
| 3 | 게이지 / 완성 크기 | 아미구루미는 게이지보다 **일정한 텐션**이 중요해서 "솜이 비치지 않게 촘촘히" 정도로만 적는 경우가 많음 |
| 4 | 약어 | 사용한 약어 목록, **US / UK 용어 중 무엇을 쓰는지** 명시 (UK dc = US sc) |
| 5 | 도안 노트 | 나선뜨기(spiral) 여부, 단 시작에 표시핀 사용, 괄호 표기 규칙 등 |
| 6 | 파츠별 도안 | 머리·몸통·팔·다리·귀 등을 **파츠마다 따로**, 단(Round) 단위로 서술 |
| 7 | 조립 | 파츠를 어느 위치에 어떤 순서로 붙이는지 |
| 8 | 마무리 / 디테일 | 자수(입·볼·눈썹), 실 정리 |

### 1.1 단(Round) 한 줄의 표기 규칙

```
R3: (sc, inc) x6 (18)
│    │          │   └─ 이 단을 마친 뒤의 총 코 수
│    │          └───── 괄호 안을 6번 반복
│    └──────────────── 짧은뜨기 1코 → 늘림 1번
└───────────────────── 3번째 단
```

- `R5–R9: sc 24 (24)` 처럼 **같은 단이 반복되면 범위**로 묶습니다.
- 대부분의 아미구루미는 **나선뜨기**(단 끝에 빼뜨기 없이 계속 뜸)로 뜨고, 단 시작에 표시핀을 꽂습니다.
- 단 중간에 들어가는 작업(색 바꾸기, 안전눈 끼우기, 솜 넣기)은 해당 단 아래 메모로 적습니다.
- 같은 위치에서 늘림을 반복하면 육각형 모양이 되므로, 늘림 위치를 엇갈리게 쓰기도 합니다.
  예: `R4: (sc, inc, sc) x6 (24)`

### 1.2 코 수 계산 원리

각 기법은 **이전 단의 코를 몇 개 쓰고(consume) 새 코를 몇 개 만드는지(produce)** 가 정해져 있습니다.
도안이 맞으려면 한 단에서 쓴 코의 합이 이전 단 코 수와 같아야 합니다.

| 기법 | 약어 (US) | 한글 | 쓰는 코 | 만드는 코 |
| --- | --- | --- | --- | --- |
| 매직링 | MR | 매직링 | – | n (첫 단) |
| 사슬뜨기 | ch | 사슬뜨기 | 0 | 1 |
| 빼뜨기 | sl st | 빼뜨기 | 1 | 1 |
| 짧은뜨기 | sc | 짧은뜨기 | 1 | 1 |
| 긴뜨기 | hdc | 긴뜨기 | 1 | 1 |
| 한길긴뜨기 | dc | 한길긴뜨기 | 1 | 1 |
| 늘림 | inc | 늘림 (한 코에 2번) | 1 | 2 |
| 줄임 | dec | 줄임 (두 코를 하나로) | 2 | 1 |
| 건너뛰기 | sk | 건너뛰기 | 1 | 0 |

`R3: (sc, inc) x6` → 쓰는 코 (1+1)×6 = 12 = R2의 코 수, 만드는 코 (1+2)×6 = **18** ✅

### 1.3 기본 도형 공식

캐릭터 파츠는 대부분 아래 기본 도형을 조합해서 만듭니다. 모델의 "형태 추정 → 도안 생성" 단계는 이 공식을 바탕으로 합니다.

| 도형 | 만드는 법 | 예 |
| --- | --- | --- |
| 원판 (평면) | 매 단 6코씩 늘림: 6 → 12 → 18 … | 발바닥, 단면 |
| 구 (공) | 최대 6k코까지 k단 늘림 → 약 k단 유지 → k−1단 줄임 → 닫기. 전체 높이는 약 **3k단** | 머리, 몸통 |
| 원기둥 | 원판으로 바닥을 만든 뒤 코 수 유지 | 팔, 다리, 목 |
| 원뿔 | 적은 코(4~6)로 시작해 2~3단마다 조금씩 늘림 | 부리, 뿔, 귀 |
| 타원체 | 구 공식에서 유지 단을 늘리거나 줄임 | 길쭉한 몸통 |
| 납작한 파츠 | 솜 없이 뜬 뒤 눌러 펴기 | 귀, 날개 |

완성 크기(cm)는 **코 수 × 코 하나 너비**로 추정합니다. 코 하나 너비는 실 굵기와 코바늘 호수에 따라 달라서 입력값(실 굵기·바늘 호수)으로 보정합니다.

---

## 2. 모델 출력 형식

모델은 **두 가지 형태**의 출력을 만듭니다.

1. **구조화 도안 (JSON)** — 모델의 1차 출력. 검증·평가·렌더링에 사용합니다. 스키마: [`pattern.schema.json`](./pattern.schema.json)
2. **사람용 도안 (Markdown / PDF)** — JSON을 렌더링한 결과물. 사용자가 실제로 보고 뜨는 문서입니다.

모델이 텍스트를 바로 쓰지 않고 JSON을 거치는 이유는, **코 수가 맞는지 기계적으로 검증**할 수 있어야 하기 때문입니다.
코 수가 틀린 도안은 실제로 뜰 수 없습니다.

### 2.1 최상위 구조

```jsonc
{
  "schema_version": "0.1",
  "meta":       { ... },   // 이름, 난이도, 완성 크기, 용어 기준
  "materials":  { ... },   // 실, 코바늘, 부자재
  "gauge":      { ... },   // 게이지 (선택)
  "notes":      [ ... ],   // 도안 노트
  "parts":      [ ... ],   // 파츠별 도안 (핵심)
  "assembly":   [ ... ],   // 조립 순서
  "details":    [ ... ]    // 자수 등 마무리 디테일
}
```

### 2.2 `meta`

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `title` | string | ✅ | 작품 이름 |
| `difficulty` | `beginner` \| `intermediate` \| `advanced` | ✅ | 난이도 |
| `finished_height_cm` | number | ✅ | 예상 완성 높이 |
| `terminology` | `US` \| `UK` | ✅ | 약어 기준. 기본값 `US` |
| `source_image` | string | | 입력 이미지 경로/ID |
| `description` | string | | 캐릭터 설명 |

### 2.3 `materials`

```jsonc
"materials": {
  "hook_mm": 3.0,
  "yarns": [
    {
      "id": "Y1",                 // 도안 전체에서 참조하는 ID
      "name": "노랑",
      "hex": "#F6D33C",           // 이미지에서 추출한 대표 색
      "weight": 3,                // CYC 표준 실 굵기 0(lace)~7(jumbo), 3 = DK
      "estimated_m": 40           // 예상 사용량 (m)
    }
  ],
  "notions": [
    { "type": "safety_eyes", "size_mm": 8, "quantity": 2 },
    { "type": "fiberfill" },
    { "type": "stitch_marker" },
    { "type": "tapestry_needle" }
  ]
}
```

`notions.type`: `safety_eyes`, `safety_nose`, `fiberfill`, `stitch_marker`, `tapestry_needle`, `pellets`, `wire`, `other`

### 2.4 `parts` — 파츠별 도안

```jsonc
{
  "id": "body",                  // 조립에서 참조하는 ID
  "name": "몸통",
  "quantity": 1,                 // 같은 파츠를 몇 개 뜨는지 (예: 귀 2개)
  "yarn": "Y1",                  // 기본 실
  "construction": "spiral",      // spiral | joined | flat
  "start": { "type": "magic_ring", "count": 6 },
  "rounds": [ ... ],
  "stuffing": "firm",            // firm | light | none
  "finish": { "type": "close" }  // close | leave_tail | fasten_off
}
```

- `construction`
  - `spiral`: 나선뜨기 (기본)
  - `joined`: 단마다 빼뜨기로 연결 (색 경계를 깔끔하게 할 때)
  - `flat`: 평면 왕복뜨기 (Row)
- `start`
  - `{ "type": "magic_ring", "count": n }`: 매직링에 n코
  - `{ "type": "chain", "count": n }`: 사슬 n코로 시작 (타원·평면)
- `finish`
  - `close`: 남은 코의 앞반코에 실을 꿰어 조여 닫기
  - `leave_tail`: 꿰맬 실을 `tail_cm`만큼 남기고 마무리
  - `fasten_off`: 바로 마무리

### 2.5 `rounds` — 단

```jsonc
{
  "from": 3, "to": 3,            // 단 범위 (같은 단 반복이면 from < to)
  "stitches": [                  // 한 단의 작업 (아래 Stitch 문법)
    { "op": "repeat", "times": 6, "body": [ { "op": "sc" }, { "op": "inc" } ] }
  ],
  "count": 18,                   // 단을 마친 뒤 코 수 (검증 대상)
  "actions": [ ... ],            // 단을 마친 뒤 할 일 (선택)
  "notes": "..."                 // 자유 메모 (선택)
}
```

**Stitch 문법** — 각 항목은 `op`를 가진 객체입니다.

| op | 추가 필드 | 의미 |
| --- | --- | --- |
| `sc`, `hdc`, `dc`, `sl_st` | `n` (기본 1), `loop` | n코 뜨기 |
| `inc`, `dec` | `n` (기본 1), `loop` | n번 늘림 / 줄임 (`dec`는 보이지 않는 줄임 기준) |
| `ch` | `n` | 사슬 n코 |
| `skip` | `n` | n코 건너뛰기 |
| `repeat` | `times`, `body` | `body`를 `times`번 반복 (중첩 가능) |
| `color` | `yarn` | 이 지점부터 다른 실로 바꾸기 (코 수 변화 없음) |

- `loop`: `both`(기본) \| `FLO`(앞반코) \| `BLO`(뒷반코)

**`actions`** — 단을 마친 뒤 할 작업

| type | 추가 필드 | 의미 |
| --- | --- | --- |
| `insert_safety_eyes` | `between_rounds`, `spacing_stitches` | 안전눈 끼우기 (닫기 전에 해야 함) |
| `stuff` | | 솜 넣기 |
| `place_marker` | `label` | 위치 표시 (조립 기준점) |

### 2.6 `assembly` — 조립

```jsonc
{
  "step": 1,
  "part": "beak",                // 붙일 파츠 ID
  "target": "body",              // 붙일 대상 파츠 ID
  "position": {
    "rounds": [10, 11],          // 대상 파츠의 단 범위
    "anchor": "front_center",    // front_center | side_left | side_right | back_center | top | bottom
    "offset_stitches": 0         // 기준점에서 몇 코 떨어졌는지
  },
  "method": "whipstitch",        // whipstitch | mattress | glue
  "instruction": "두 눈 사이 가운데, 10~11단에 꿰매기"
}
```

### 2.7 `details` — 디테일

```jsonc
{
  "type": "embroidery",          // embroidery | felt | other
  "target": "body",
  "feature": "cheeks",
  "yarn": "Y3",
  "position": { "rounds": [11, 11], "anchor": "front_center", "offset_stitches": 5 },
  "instruction": "눈 바깥쪽 아래에 2코 너비로 가로 자수, 양쪽"
}
```

---

## 3. 검증 규칙

모델이 생성한 JSON은 아래 규칙을 모두 통과해야 **유효한 도안**입니다.
[`validate_pattern.py`](./validate_pattern.py)로 검사할 수 있습니다.

| # | 규칙 | 설명 |
| --- | --- | --- |
| V1 | 스키마 | `pattern.schema.json` 구조를 따름 |
| V2 | 단 연속성 | 단 범위가 1부터 빈틈·겹침 없이 이어짐 |
| V3 | 코 사용 일치 | 각 단에서 **쓰는 코 합 = 이전 단 코 수** (매직링 첫 단 제외) |
| V4 | 코 수 일치 | 각 단에서 **만드는 코 합 = `count`** |
| V5 | 범위 단 | `from < to`인 단은 코 수가 변하지 않아야 함 (늘림·줄임 없음) |
| V6 | 참조 무결성 | `yarn`, `part`, `target` ID가 실제로 존재 |
| V7 | 순서 제약 | `insert_safety_eyes`는 `close` 전 단에 있어야 하고, 솜을 넣는 파츠는 닫기 전에 `stuff`가 있어야 함 |
| V8 | 조립 위치 | `position.rounds`가 대상 파츠의 단 범위 안에 있음 |

> 사슬로 시작하는 파츠(`start.type = chain`)의 첫 단은 사슬 양쪽을 돌아 뜨기 때문에 V3 검사를 건너뜁니다.

---

## 4. 사람용 도안 렌더링 규칙

JSON을 아래 형식의 문서로 렌더링합니다. 한국어(기본)와 영어(US)를 지원합니다.

### 4.1 문서 구성

```
# {title}
완성 크기 · 난이도 · 용어 기준

## 재료
## 게이지
## 약어
## 도안 노트
## 파츠별 도안
### {파츠 이름} ×{quantity} ({실 이름})
## 조립
## 마무리
```

### 4.2 단 표기

| JSON | 한국어 | English (US) |
| --- | --- | --- |
| `start: magic_ring 6` + R1 | `R1: 매직링에 짧은뜨기 6 (6)` | `R1: 6 sc in MR (6)` |
| `inc ×6` | `R2: 늘림 ×6 (12)` | `R2: inc x6 (12)` |
| `repeat 6 [sc, inc]` | `R3: (짧은뜨기 1, 늘림) ×6 (18)` | `R3: (sc, inc) x6 (18)` |
| `from 7 to 12, sc 36` | `R7–R12: 짧은뜨기 36 (36)` | `R7–R12: sc 36 (36)` |
| `color Y2` | `[Y2로 색 바꾸기]` | `[change to Y2]` |
| `loop BLO` | `뒷반코에 짧은뜨기` | `BLO sc` |
| `actions: stuff` | `→ 솜 채우기` | `→ Stuff firmly.` |

- 마지막 괄호 `(n)`에는 항상 그 단의 총 코 수를 적습니다.
- `actions`는 해당 단 아래에 `→`로 시작하는 줄로 씁니다.
- 약어 섹션에는 **실제로 쓴 기법만** 나열합니다.

### 4.3 예시

- 구조화 도안: [`examples/chick.pattern.json`](./examples/chick.pattern.json)
- 사람용 도안: [`examples/chick.pattern.md`](./examples/chick.pattern.md)

---

## 5. 평가 관점 (향후)

| 항목 | 측정 방법 |
| --- | --- |
| 유효성 | 검증 규칙 V1~V8 통과율 |
| 형태 유사도 | 도안으로 만든 3D 모델(시뮬레이션)과 입력 이미지의 실루엣 비교 |
| 색상 정확도 | 추천 실 색상과 원본 이미지 색상의 색차 (ΔE) |
| 난이도 적합성 | 난이도별 허용 기법·파츠 수 준수 여부 |
| 실제 제작 | 직접 떠서 완성품과 원본 비교 (정성 평가) |
