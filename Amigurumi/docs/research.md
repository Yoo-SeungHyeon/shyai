# 선행 연구 및 기술 조사

Amigurumi의 아키텍처를 정하기 위해 조사한 기존 연구·도구·모델과, 각각이 설계에 주는 시사점을 정리합니다.
조사일: 2026-11-01

> ⚠️ 조사 환경에서 arXiv 본문에 접근할 수 없어 일부 논문은 초록과 2차 요약으로 확인했습니다. **2차 요약으로만 확인한 수치는 _(2차)_ 로 표시**했고, 구현 전에 원문으로 다시 확인해야 합니다.

---

## 1. 핵심 질문과 결론 요약

| 질문 | 결론 | 근거 |
| --- | --- | --- |
| LLM/VLM이 이미지를 보고 도안을 바로 쓰게 하면 되나? | **안 된다.** 실행 가능한 도안을 만드는 비율이 매우 낮다 | CrochetBench, 사용자 사례 (§2) |
| 3D 형태 → 도안 변환은 풀린 문제인가? | **결정론적 알고리즘으로 가능함이 입증됐다** | AmiGo, Stitch Meshes for Crochet (§3) |
| 이미지 → 3D는 쓸 만한가? | 오픈 모델로 가능. 단 **라이선스와 GPU 조건** 확인이 필요하다 | TRELLIS.2, TripoSR, Hunyuan3D (§4) |
| 파츠(머리·귀·팔) 분리는? | 이미지에서 바로 파츠별 3D를 만드는 모델과, 3D를 나중에 나누는 모델이 모두 있다 | PartCrafter, OmniPart, PartField, SAMPart3D (§4) |
| 도안이 맞는지 형태로 검증할 수 있나? | 크로셰 시뮬레이터가 있고, **렌더 이미지 비교**를 평가에 쓴 선례가 있다 | CrochetPARADE, CrochetBench (§5) |
| 같은 목표의 프로젝트가 있나? | 있다. 신경망 없이 **결정론적 검증**을 중심에 둔 구조다 | CrochetPhoto2Pattern (§6) |

**설계 결론:** 신경망은 **"이미지 이해(형태·파츠·색)"** 에만 쓰고, **코 수 계산은 결정론적 알고리즘**이 맡는다. 생성한 도안은 **시뮬레이션해서 입력 이미지와 비교**한다.
→ 자세한 구조는 [architecture.md](./architecture.md) 참고

---

## 2. LLM / VLM으로 도안을 직접 생성하는 접근

### 2.1 CrochetBench (Li et al., ACL 2026)

VLM이 크로셰를 **"설명"하는 수준에서 "실행 가능한 도안을 만드는" 수준**으로 갈 수 있는지 평가한 벤치마크입니다.

- **과제 4개:** 스티치 인식, 도안 선택(객관식), 이미지 → 자연어 도안 생성, 자연어 → CrochetPARADE DSL 변환
- **데이터:** Yarnspirations 계열 브랜드 도안. 생성 과제는 학습 4,859 / 검증 274 / 테스트 877
- **평가 모델:** GPT-4o, Gemini 2.5 Flash-Lite, Claude Sonnet 4, Qwen2-VL 7B, DeepSeek-VL 7B, Gemma 3 4B, BLIP-2
- **평가 방법:** DSL로 바꾼 도안이 **검증을 통과하고 실제로 실행되는지(Valid Pattern Rate)**, 그리고 시뮬레이터 렌더와 정답 이미지의 **DINO 유사도**
- **주요 결과**
  - 인식은 어느 정도 되지만 **실행 가능한 도안 생성은 크게 떨어진다.**
  - 모델이 클수록 오히려 유효율이 낮은 경우가 있었다. DSL에 없는 기법을 지어내기 때문이다.
  - 파인튜닝하면 BLEU 같은 텍스트 점수는 오르지만 **실행 정확도는 오르지 않았다.**
  - 프로젝트 단위 DSL 생성 성공률은 상용 모델 4~5%, Qwen2-VL 21% 수준 _(2차)_
- **데이터 라이선스:** CC BY-NC 4.0, 연구·개인 용도만 허용

**시사점**
- 신경망이 코 수를 직접 쓰게 하는 구조는 피한다. 학습 데이터를 늘리거나 파인튜닝해도 해결된다는 근거가 없다.
- "렌더해서 이미지로 비교한다"는 평가 방식은 그대로 가져온다.

### 2.2 범용 챗봇 사례

- ChatGPT·Gemini로 아미구루미 도안을 만들어 본 사례들은 공통적으로 **코 수 불일치**, **파츠 크기·부착 위치 오류**, **파츠 누락**을 보고합니다 (Wired, abcrafty).
- AI로 만든 도안을 판매하는 사례에서도 "사진과 도안 결과물이 다르다"는 구매자 리뷰가 확인됩니다.

**시사점:** 사람이 단마다 코 수를 직접 검산해야 한다면 이 모델이 존재할 이유가 없다. **검증을 통과한 도안만 출력**해야 한다.

---

## 3. 3D 형태 → 크로셰 도안 (계산 설계)

### 3.1 AmiGo (Edelstein, Peleg, Itzhaky, Ben-Chen — ACM SCF 2022)

아미구루미 도안 생성의 대표 논문입니다.

- **입력:** 닫힌 삼각형 메시 + 사용자가 찍은 시작점 1개
- **출력:** 떠서 솜을 넣으면 입력 형태와 비슷해지는 크로셰 도안
- **방법**
  1. 메시 위에 **Crochet Graph**(코의 위치와 연결)를 만든다.
  2. 이를 크로셰 도안으로 번역한다.
  3. 형태를 **뜰 수 있는 조각들로 자동 분할**하고, 꿰매지 않고 이어서 뜨는 방식(join-as-you-go)으로 연결한다.
- **결과:** 다양한 형태에 적용되고 실제로 뜨기 쉬운 도안이 나온다고 보고
- **코드 공개 여부:** 이번 조사에서는 확인하지 못함

**시사점**
- **"3D 형태만 있으면 결정론적으로 도안을 만들 수 있다"** 는 근거가 된다.
- 다만 AmiGo는 한 덩어리 메시를 대상으로 한다. 캐릭터 아미구루미는 대개 **파츠를 따로 떠서 꿰매는 방식**이라, 파츠 단위로 단순화한 버전이 우리 목적에 더 맞다.

### 3.2 Representing Crochet with Stitch Meshes (Guo, Lin, Narayanan, McCann — ACM SCF 2020)

- 니트용 Stitch Mesh 기법(Yuksel et al., SIGGRAPH 2012)을 크로셰로 확장했다.
- 바늘에 걸린 고리를 표현하는 새 edge 타입과 크로셰 기법별 face 라이브러리를 정의했다.
- 3D 모델에서 Craft Yarn Council 표기법의 도안을 생성하고 결과 형태를 시뮬레이션한다.

**시사점:** 늘림/줄임 외에 hdc·dc 같은 기법, 반코뜨기까지 다루려면 이런 **코 단위 표현**이 필요하다. v0.x 범위 밖으로 둔다.

### 3.3 Knitty (Y. Igarashi, T. Igarashi, Suzuki — Eurographics 2008)

- 스케치로 뜨개 동물 인형의 3D 모양을 만들면 뜨개 도안을 만들어 주는 시스템이다.
- 초보자 워크숍에서 아이들도 자기 인형을 디자인할 수 있었다고 보고했다.
- AmiGo 논문은 이 계열 방법을 "메시를 일정 간격의 나선 띠로 덮고, 일정 거리마다 샘플링해서 도안을 계산한다"고 소개한다.

**시사점:** 축을 따라 일정 간격으로 단을 나누고 단마다 둘레를 재서 코 수를 정하는 방식은 오래 검증된 접근이다. 우리의 "회전체 프로파일" 방식(architecture.md §4)이 이 계열에 속한다.

### 3.4 Neural Inverse Knitting (Kaspar et al., ICML 2019)

- 니트 원단 사진 한 장 → 니트 기계 명령어(DSL)를 예측하는 신경망
- 실제 사진 데이터가 부족해서 **니트 시뮬레이터로 만든 합성 데이터**로 보강했다.
- "실제 사진을 합성 이미지처럼 보이게 바꾸는 것"이 성능에 도움이 됐다.

**시사점:** 신경망이 뜨개 명령을 직접 예측해야 한다면 **시뮬레이터로 합성 데이터를 만드는 것**이 핵심이다. 우리도 시뮬레이터를 먼저 만들어 두면 이후 학습 단계(파츠 분해 모델 등)에서 합성 데이터를 만들 수 있다.

---

## 4. 이미지 → 3D, 파츠 분해

### 4.1 이미지 → 3D 생성 모델

| 모델 | 개발 | 라이선스 | 요구 사양 | 특징 |
| --- | --- | --- | --- | --- |
| **TRELLIS.2** | Microsoft | MIT | NVIDIA GPU 24GB 이상, Linux | 4B 파라미터. GLB + PBR 텍스처 출력. H100 기준 512³ 해상도 약 3초 |
| **TripoSR** | Stability AI · Tripo | MIT | 가벼움 | 0.5초 이내로 빠름. 품질은 신형 모델보다 낮음 |
| **Hunyuan3D 2.1** | Tencent | Tencent Community License | 형상 10GB, 전체 29GB | 품질이 좋다는 평가. **라이선스 적용 지역에서 한국·EU·영국 제외** |

**시사점**
- **Hunyuan3D는 한국에서 쓸 수 없다.** 라이선스 지역에서 대한민국이 제외되어 있다.
- 기본 후보는 **TRELLIS.2(품질)** 와 **TripoSR(빠른 시험·저사양)** 이다. 둘 다 MIT 라이선스다.
- 모듈을 교체할 수 있게 설계해서 더 나은 모델이 나오면 바꾼다.

### 4.2 파츠 단위 3D

| 모델 | 방식 | 비고 |
| --- | --- | --- |
| **PartCrafter** (NeurIPS 2025) | 이미지 1장 → **여러 파츠 메시를 동시에 생성**. 입력에서 가려진 파츠도 생성 | 코드·학습 데이터 공개 |
| **OmniPart** (2025) | 2D 파츠 마스크 → 3D 바운딩 박스 배치 → 파츠별 생성. 파츠 크기를 사용자가 정할 수 있음 | |
| **PartField** (NVIDIA, ICCV 2025) | 완성된 3D에 **파츠 분할**을 적용. 한 번의 추론으로 빠름 | 벤치마크 mIoU 59.1, 형상당 약 10초 _(2차)_ |
| **SAMPart3D** (2024) | 학습된 라벨 없이 여러 크기 단위로 분할 | mIoU 56.2, 형상당 약 15분 _(2차)_ |

**시사점:** 아미구루미는 파츠별로 따로 뜨기 때문에 **파츠 분해가 파이프라인의 핵심 중간 단계**다. 두 경로를 비교한다.
- (A) PartCrafter처럼 처음부터 파츠별로 생성
- (B) TRELLIS.2로 통 메시를 만든 뒤 PartField로 분할

### 4.3 공통 한계

- 사진 한 장으로는 **뒷면, 깊이, 실제 크기**를 알 수 없다. 생성 모델이 "그럴듯하게" 채워 넣을 뿐이다.
- 캐릭터 일러스트(2D 데포르메)는 실사 사진보다 3D 복원이 어렵다. 이 부분은 직접 실험해서 확인해야 한다.

---

## 5. 크로셰 시뮬레이션

### 5.1 CrochetPARADE (Svetlin Tassev)

- 크로셰 도안 전용 언어(DSL) + 2D/3D 렌더러 + 분석·디버거
- 브라우저에서 three.js로 3D를 보여주고, 너무 당기거나 느슨한 코를 찾아준다.
- 3D 모델을 Blender용으로 내보낼 수 있다 (glTF로 추정). 문법 자체는 퍼블릭 도메인이다.
- **라이선스: GPLv3**. 코드를 우리 프로젝트에 포함하면 GPL 의무가 생긴다.
- 코가 수만 개인 도안은 계산에 몇 분 이상 걸린다.
- CrochetBench와 CrochetPhoto2Pattern이 모두 이 DSL을 실행 가능한 중간 표현으로 쓴다.

**시사점**
- 우리 JSON을 **CrochetPARADE DSL로 내보내는 기능**을 만들면, 코 단위의 정밀한 시뮬레이션을 외부 도구로 검증할 수 있다.
- GPL 문제를 피하려고 코드를 포함하지 않고 **내보내기 형식만 맞춘다**. 문법은 퍼블릭 도메인이다.
- 빠른 내부 검증용으로는 자체 경량 시뮬레이터(회전체)를 따로 둔다.

---

## 6. 같은 목표의 프로젝트: CrochetPhoto2Pattern

사진 → 아미구루미 도안을 목표로 하는 오픈소스(MIT, 베타)입니다. 우리와 목표가 가장 가깝습니다.

- **파이프라인:** 사진 → 기하·의미 관찰 → 사용자가 목표 크기 입력 → 파츠 구조 → 크로셰 파라미터 → **결정론적 검증** → 사용자 수정 → 내보내기
- **클라우드 LLM/VLM을 의도적으로 제거**했다. 로컬 비전(GrabCut 분할, 선택적 포즈 랜드마크)만 쓴다.
- **3D 복원은 하지 않는다.** 미리 정한 파츠 템플릿에 비율만 맞춘다.
- 사용자가 윤곽, 머리 영역, 파츠 이름을 직접 확인·수정하는 단계가 있다.
- 출력은 Markdown, PDF, 링 차트, 색상별 재료표, JSON, **CrochetPARADE DSL**
- **실물 시험 기록 도구**가 있다. 도안 해시, 게이지, 완성 치수, 실을 기록해서 상수를 보정한다.
- 근거 수준을 스스로 나눠서 밝힌다.
  1. 구조적 정확성: 자동 검증으로 보장
  2. 다양한 사진에 대한 일반화: 미확인
  3. 실제로 떴을 때 맞는지: 미확인

**시사점**
- "결정론적 검증 + 사용자 확인 단계 + 실물 시험으로 보정"은 그대로 참고한다.
- 차별점: 템플릿 대신 **3D 복원 + 파츠 분해**로 임의의 캐릭터 형태에 대응한다. 템플릿 방식은 사람 모양이 아닌 캐릭터에 약하다.
- 이 프로젝트처럼 **어떤 근거 수준까지 확인됐는지**를 버전마다 밝힌다.

---

## 7. 데이터

| 소스 | 내용 | 사용 가능성 |
| --- | --- | --- |
| CrochetBench | 크로셰 도안 + 이미지 약 6천 개 | CC BY-NC 4.0, **연구용만** |
| StitchSwitch (AAAI 심포지엄) | 사용자 도안 → CrochetPARADE 번역 109개 | 공개 (규모 작음) |
| Ravelry | 최대 규모 도안 DB, API 있음 | **ML 학습 허용 여부를 확인하지 못함.** 약관 검토 전 사용 금지 |
| 자체 합성 데이터 | 시뮬레이터로 (도안 → 3D → 렌더) 쌍을 생성 | 제한 없음. **기본 전략** |

**시사점:** v0.x 파이프라인은 사전학습 모델과 결정론적 알고리즘으로 구성하므로 **자체 학습 데이터가 없어도 동작한다**. 나중에 학습이 필요해지면(예: 데포르메 캐릭터 파츠 분해 파인튜닝) 합성 데이터를 먼저 쓴다.

---

## 8. 추가로 확인할 항목

- [ ] AmiGo 원문: 단 간격·코 크기 가정, 솜 넣은 뒤 형태 변화를 어떻게 보정하는지, 코드 공개 여부
- [ ] CrochetBench 원문 표: 모델별 Valid Pattern Rate 정확한 수치
- [ ] PartField · PartCrafter 라이선스 (상업적 이용 가능 여부)
- [ ] 캐릭터 일러스트 입력에서 TRELLIS.2 / TripoSR / PartCrafter 품질 비교 (직접 실험)
- [ ] Ravelry API 약관의 데이터 활용 조항
- [ ] 실물 기준 코 크기: 실 굵기·바늘 호수별 짧은뜨기 1코의 너비와 높이 (직접 게이지 측정)

---

## 참고 자료

- AmiGo: [arXiv 2211.01178](https://arxiv.org/abs/2211.01178) · [Hugging Face Papers](https://huggingface.co/papers/2211.01178) · DOI 10.1145/3559400.3562005
- Representing Crochet with Stitch Meshes: [Textiles Lab](https://textiles-lab.github.io/publications/2020-crochet-meshes) · [SIGGRAPH History](https://history.siggraph.org/?p=82596)
- Stitch Meshes (Yuksel et al. 2012): [PDF](https://research.cs.cornell.edu/stitchmeshes/stitchmeshes.pdf)
- Knitty: [프로젝트 페이지](https://www.is.ocha.ac.jp/~yuki/knitty/index-e.html) · [Eurographics Digital Library](https://diglib.eg.org/items/3f313726-d818-4525-b19c-a59fd47a7945)
- Neural Inverse Knitting: [프로젝트 페이지](https://deepknitting.csail.mit.edu) · [PMLR](https://mlanthology.org/icml/2019/kaspar2019icml-neural)
- CrochetBench: [arXiv 2511.09483](https://arxiv.org/html/2511.09483v2) · [ACL Anthology](https://aclanthology.org/2026.acl-long.604/) · [GitHub](https://github.com/Peiyu-Georgia-Li/crochetBench) · [2차 요약](https://www.themoonlight.io/en/review/crochetbench-can-vision-language-models-move-from-describing-to-doing-in-crochet-domain)
- StitchSwitch: [AAAI-SS](https://ojs.aaai.org/index.php/AAAI-SS/article/download/36054/38209/40142)
- CrochetPARADE: [GitHub](https://github.com/stassev/CrochetPARADE) · [crochetparade.org](https://www.crochetparade.org/)
- CrochetPhoto2Pattern: [GitHub](https://github.com/paulkooer/CrochetPhoto2Pattern)
- TRELLIS.2: [GitHub](https://github.com/microsoft/TRELLIS.2)
- TripoSR: [Papers with Code](https://PapersWithCode.com/paper/triposr-fast-3d-object-reconstruction-from-a)
- Hunyuan3D 2.1: [LICENSE](https://gitserver.onethingai.com/ai-models/Hunyuan3D-2.1/raw/branch/main/LICENSE) · [사양 정리](https://docs.clore.ai/guides/3d-generation/hunyuan3d)
- PartCrafter: [NeurIPS 2025](https://neurips.cc/virtual/2025/poster/120299)
- OmniPart: [arXiv 2507.06165](https://fugumt.com/fugumt/paper_check/2507.06165v1_enmode)
- PartField: [NVIDIA](https://research.nvidia.com/labs/toronto-ai/partfield-release) · [논문 요약](https://en.papernotes.org/ICCV2025/segmentation/partfield_learning_3d_feature_fields_for_part_segmentation_and_beyond/)
- SAMPart3D: [프로젝트 페이지](https://yhyang-myron.github.io/SAMPart3D-website)
- AI 도안 사례: [Wired](https://wirednews.pages.dev/story/chatgpt-crochet) · [abcrafty](https://abcrafty.com/ai-crochet-patterns/)
- Craft Yarn Council 표준: [Standards and Guidelines](https://www.craftyarncouncil.com/?q=node/7)
