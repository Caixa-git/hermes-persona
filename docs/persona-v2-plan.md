---
name: persona-v2-plan
description: "📋 Hermes Persona v2 — task analysis → role matching → intelligent routing. Academic framework-based role selection system design."
---

# 📋 Hermes Persona v2 Design

직무 심리학 + 인지 과학 프레임워크 기반의 지능형 역할 선택 시스템.

---

## 1. 현재 시스템의 한계

현재는 README 문자열 매칭에 의존한다. 워커가 `curl`로 카탈로그를 읽고 직관적으로 판단한다.

| 한계 | 영향 |
|------|------|
| 단일 역할만 할당 가능 | 복잡한 태스크는 여러 전문가가 필요 |
| 역할 선택이 LLM의 직관에 의존 | 일관성 부족, 재현성 낮음 |
| 태스크 분석 없이 역할 검색 | 잘못된 역할 선택 가능성 |
| 학습 루프 없음 | 같은 실패 반복 가능 |

---

## 2. 적용 가능한 학술 프레임워크

### Holland's RIASEC (직업 선택 이론, 1959)

6가지 성격 유형으로 모든 직무를 분류:

| 유형 | 성향 | agency-agents 매핑 |
|------|------|-------------------|
| **R**ealistic | 실제적, 손으로 하는 일 | Engineering, DevOps, Embedded |
| **I**nvestigative | 탐구적, 분석, 연구 | Academic, Research, Security |
| **A**rtistic | 예술적, 창의적 | Design, Content, Creative |
| **S**ocial | 사회적, 도움, 교육 | Support, Customer Service |
| **E**nterprising | 진취적, 설득, 리더십 | Sales, Marketing, Product |
| **C**onventional | 관습적, 체계적, 조직 | PMO, Finance, Operations |

→ 각 역할에 RIASEC 코드를 부여하면 태스크 분석 후 유사도 기반 매칭 가능.

### Job Characteristics Model (Hackman & Oldham, 1976)

5가지 핵심 특성으로 직무의 동기부여 잠재력 평가:

| 특성 | 설명 | 컨반 워커에 적용 |
|------|------|-----------------|
| Skill Variety | 다양한 기술 필요도 | 풀스택 vs 단순 CRUD |
| Task Identity | 완결된 업무 단위 | 하나의 칸반 태스크 = 1 Identity |
| Task Significance | 영향력의 크기 | 프로덕션 배포 vs 내부 스크립트 |
| Autonomy | 자율성 수준 | 태스크 바운더리 내 자유도 |
| Feedback | 결과 명확성 | kanban_complete의 핸드오프 품질 |

→ 중요도가 낮고 자율성이 높은 태스크는 시니어 역할에, 반대는 주니어 역할에 매칭.

### Person-Job Fit (Edwards, 1991)

두 가지 매칭 방식:

```
Demands-Abilities Fit  (DA Fit):
  태스크가 요구하는 것 ← → 워커/역할이 제공하는 능력

Needs-Supplies Fit    (NS Fit):
  태스크가 제공하는 것 ← → 워커/역할이 원하는 것
```

AI 워커에게 NS Fit은 무의미. **DA Fit만이 중요**.
→ 역할 선택 = 태스크 요구사항을 가장 잘 충족하는 역할 찾기.

### 인지 부하 이론 (Sweller, 1988)

세 가지 인지 부하 유형:

| 유형 | 설명 | 역할 설계에 적용 |
|------|------|-----------------|
| 내재적 (Intrinsic) | 태스크 자체의 복잡도 | 복잡한 태스크 → 아키텍트 |
| 외재적 (Extraneous) | 불필요한 정보 처리 | 검증된 .md = 외재적 부하 감소 |
| 본질적 (Germane) | 학습과 스키마 형성 | 역할 반복 → 패턴 학습 |

→ 잘 설계된 .md 템플릿은 외재적 부하를 최소화하고 본질적 부하를 최대화.

### 역할 이론 (Biddle, 1986)

```
역할 기대(Role Expectation) → 역할 수행(Role Performance) → 역할 평가(Role Evaluation)

Persona SKILL.md → 워커가 역할 채택 → kanban_complete 핸드오프
```

키 포인트: **역할 명세가 구체적일수록 역할 수행의 질이 높아진다.**

---

## 3. 제안: 다차원 태스크 분석 엔진

### 3.1 태스크 분석 차원

모든 태스크를 5개 차원으로 분석:

```
Dimension 1: Domain (도메인)
  engineering, design, marketing, sales, support, 
  product, project-management, testing, academic, finance

Dimension 2: Activity Type (활동 유형)
  CREATE (생성) | ANALYZE (분석) | MANAGE (관리)
  RESEARCH (연구) | COMMUNICATE (소통) | OPTIMIZE (최적화)

Dimension 3: Output Type (산출물 유형)
  code, document, design, data, strategy, infrastructure

Dimension 4: Tech Stack (기술 스택)
  React, Python, AWS, PostgreSQL, iOS, etc.

Dimension 5: Complexity (복잡도)
  1 (단순) ~ 5 (매우 복잡)
```

### 3.2 역할 프로파일 행렬

각 역할을 5차원 벡터로 표현:

```
Backend Architect:
  domain:      [engineering: 1.0]
  activity:    [CREATE: 0.6, OPTIMIZE: 0.4]
  output:      [code: 0.5, infrastructure: 0.3, data: 0.2]
  tech:        [API, database, cloud, auth]
  complexity:  [3-5]

Frontend Developer:
  domain:      [engineering: 1.0]
  activity:    [CREATE: 0.7, OPTIMIZE: 0.3]
  output:      [code: 0.8, design: 0.2]
  tech:        [React, Vue, Angular, CSS, UI]
  complexity:  [2-4]
```

### 3.3 매칭 알고리즘

```
태스크 T의 벡터 V_t = (domain, activity, output, tech, complexity)

각 역할 R_i의 벡터 V_i = (domain, activity, output, tech, complexity)

유사도 점수 S(T, R_i) = w₁ × cos(V_t.domain, V_i.domain)
                       + w₂ × cos(V_t.activity, V_i.activity)
                       + w₃ × cos(V_t.output, V_i.output)
                       + w₄ × tech_overlap(V_t.tech, V_i.tech)
                       + w₅ × complexity_fit(V_t.complexity, V_i.complexity)

Top-3 역할 반환 (confidence score 포함)
```

### 3.4 태스크 분해 (멀티 역할)

복잡도 3 이상의 태스크 → 자동 분해:

```
Input: "Build a web app with React frontend, Node.js backend,
        PostgreSQL database, deploy on AWS"

→ Sub-task 1: 🎨 Frontend (React UI)
→ Sub-task 2: 🏗️ Backend (Node.js API)
→ Sub-task 3: 🗄️ Database (Schema + queries)
→ Sub-task 4: 🚀 DevOps (AWS CI/CD)

→ kanban_create × 4 (with parent dependency chain)
```

---

## 4. 실행 계획

### Phase 1: 태스크 분류기 (현재 단계)

```
워커가 README를 읽고 직관적으로 역할 선택
→ LLM의 내재적 분류 능력 활용
→ 충분히 좋은 결과 (테스트 통과율 100%)
```

### Phase 2: 구조화된 역할 프로파일

```
각 역할의 5차원 프로파일을 SKILL.md에 포함
→ CANI (context-aware natural instructions) 포맷으로 저장
→ 워커가 태스크 분석 후 점수 기반 선택
```

### Phase 3: 학습 루프

```
kanban_complete의 핸드오프 메타데이터 수집
→ 역할 선택의 정확도 피드백
→ 프로파일 가중치 w₁~w₅ 최적화
→ 실패 패턴 학습 및 회피
```

### Phase 4: 멀티 역할 오케스트레이션

```
단일 태스크 → 분석 → sub-task 분해
→ 각 sub-task에 최적 역할 할당
→ 의존성 그래프 기반 순차/병렬 실행
→ 통합 결과 리포팅
```

---

## 5. 구체적 제안: CANI 프로파일 확장

각 역할 .md의 YAML frontmatter에 추가할 메타데이터:

```yaml
---
name: Backend Architect
description: "..."
emoji: 🏗️
vibe: "..."
# --- 아래는 다차원 프로파일 ---
profile:
  domain: engineering
  activity: [create: 0.6, optimize: 0.3, analyze: 0.1]
  output: [code: 0.5, infra: 0.3, data: 0.2]
  tech_tags: [api, rest, graphql, database, postgresql, 
              mysql, redis, docker, kubernetes, aws, auth]
  complexity: [3, 4, 5]
  riasec: [R: 0.7, I: 0.2, C: 0.1]
  jcm:
    skill_variety: 4
    task_identity: 3
    task_significance: 4
    autonomy: 3
    feedback: 3
---
```

이 데이터는 원본 .md를 수정하지 않고, 별도의 인덱스 파일(`~/.hermes/persona-index.yaml`)로 관리.

---

## 6. 결론

| 현재 (v1) | 제안 (v2) |
|-----------|-----------|
| 문자열 직관 매칭 | 다차원 벡터 유사도 |
| 단일 역할 | 멀티 역할 분해 |
| 피드백 없음 | 학습 루프 |
| LLM 의존 | 구조화된 메타데이터 |
| 수동 선택 | 점수 기반 자동 추천 |

v2의 핵심 통찰: **"모든 태스크는 5차원 공간의 점이고, 모든 역할은 그 공간의 영역이다. 매칭은 가장 가까운 영역을 찾는 기하 문제다."**
