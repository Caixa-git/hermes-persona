# Requirements + Technical Spec — hermes-persona

**작성:** 2026-05-06
**워커:** persona-worker (추천: 🏛️ Software Architect + 📋 Product Manager, S=2)
**아니마:** System Thinker — High C, High O, Low E

---

**입력 자료:** `DISCOVERY_BRIEF.md`

---

## 1. 제품 목표

hermes-persona는 Hermes Agent의 kanban worker에게 적절한 전문가 역할(페르소나)을 자동 선택해주는 스킬 패키지.

### 핵심 가치 제안
- 172개 전문가 역할 카탈로그에서 최적 역할 자동 선택
- 역할 불일치 시 일반론자 폴백 (40-50% 품질 저하 방지)
- Anima(본질) > Persona(역할) 우선순위 체계
- 단일/멀티 페르소나 자동 판단 (CDPD 모델)

✅ 확인된 사실

## 2. 기능 요구사항

### 필수 (Must)

| ID | 요구사항 | 현재 상태 | 완료 기준 |
|----|---------|-----------|-----------|
| F1 | 역할 카탈로그 조회 | ✅ SHA-pinned curl + 로컬 캐시 | 오프라인 fallback 동작 |
| F2 | 단일 페르소나 선택 | ✅ 10-step 프로토콜 | heartbeat에 역할 표시 |
| F3 | 멀티 페르소나 (주+부) | ✅ CDPD S≥2 | heartbeat에 main+minor 표시 |
| F4 | Anima > Persona 우선순위 | ✅ Layer 13, SKILL.md 명시 | 실험 검증 완료 |
| F5 | 일반론자 폴백 (<30%) | ✅ confidence threshold | heartbeat에 fallback 사유 표시 |
| F6 | 게이트웨이 신원 주입 | ✅ GATEWAY_ANIMA_PERSONA_IDENTITY | run_agent.py에서 자동 주입 |
| F7 | 설치 스크립트 | ✅ install.sh | --dry-run/--uninstall 지원 |

✅ 확인된 사실

### 권장 (Should)

| ID | 요구사항 | 현재 상태 | 우선순위 근거 |
|----|---------|-----------|---------------|
| F8 | PyPI 배포 | ❌ 미지원 | pip install 가능해짐, 사용자 접근성 향상 |
| F9 | install.sh 단위 테스트 | ❌ 없음 | 설치 실패 감지 불가 |
| F10 | develop 브랜치 정리 | ❌ stale | 협업자 혼선 유발 |

📐 합리적 추정

### 고려 가능 (Could)

| ID | 요구사항 | 비고 |
|----|---------|------|
| F11 | 역할 카탈로그 오프라인 완전 캐시 | 현재 clone --depth=1, 주기적 갱신 필요 |
| F12 | CDPD 파라미터 자동 교정 | 새 모델 등장 시 Φ/α/β 재계산 필요 |

💭 가정

## 3. 품질 속성 (FURPS+)

| 속성 | 목표 | 현재 | 갭 |
|------|------|------|-----|
| **안정성** | 설치 100% 성공 | 18/18 테스트 통과 | install.sh 단위 테스트 없음 |
| **성능** | 역할 선택 <5초 | 로컬 캐시 시 <1초 | 네트워크 fallback 시 지연 |
| **보안** | credential 0 노출 | SECURITY_AUDIT.md 확인 | 미검증 |
| **유지보수성** | 문서 현행화 | README/refs 양호 | CHANGELOG 없음 |
| **사용성** | `--skill persona` 1줄 | kanban_create 플래그 | CLI 피드백 개선 여지 |

✅ 확인된 사실 / 📐 합리적 추정

## 4. 기술 구조

```
사용자 → Gateway Agent (메카 위진수)
              │
              │ kanban_create(skills=["persona"])
              ▼
       persona-worker
              │
              ├─ 1. kanban_show() → task 분석
              ├─ 2. CDPD 평가 (S 값 계산)
              ├─ 3. agency-agents 카탈로그 조회 (로컬 → GitHub fallback)
              ├─ 4. 역할 채택 (heartbeat)
              ├─ 5. hermes-anima 프로필 로드
              └─ 6. 작업 실행 (nature > role)
```

### 의존성

| 의존성 | 버전 고정 | 장애 모드 |
|--------|-----------|-----------|
| msitarzewski/agency-agents @ 783f6a72 | SHA-pinned | no-role fallback (무음) |
| Caixa-git/hermes-anima @ 9cfba350 | SHA-pinned | 일반론자 폴백 |
| Hermes Agent (kanban 시스템) | 런타임 | 작업 생성 불가 |

✅ 확인된 사실

## 5. 기술 부채

| 항목 | 유형 (Fowler 기준) | 영향 |
|------|-------------------|------|
| PyPI 미배포 | Prudent deliberate | pip install 불가 |
| develop 브랜치 방치 | Inadvertent | 협업 시 혼선 |
| install.sh 단위 테스트 부재 | Reckless deliberate | 설치 실패 조기 감지 불가 |
| CHANGELOG 부재 | Prudent deliberate | 릴리즈 내역 추적 불가 |

📐 합리적 추정

---

## 완료 기준 체크

| 조건 | 상태 | 근거 |
|------|------|------|
| 기능 완성 | ✅ | F1-F7 모두 동작 |
| 회귀 제로 | ✅ | 18/18 통과 |
| 문서 현행화 | ✅ | README + 8개 references |
| 보안 기본 | 🟡 | SECURITY_AUDIT.md 갱신됨, 정기 감사 필요 |
| 릴리즈 이력 | 🟡 | v1.0.0 태그 존재, CHANGELOG 없음 |

---

## 다음 Step 입력값

- `DISCOVERY_BRIEF.md`
- `REQUIREMENTS_AND_SPEC.md` (본 문서)
- 필수 기능 F1-F7, 권장 F8-F10
- 기술 부채 4건
- 완료 기준: 기능 5/5 🟢, 이력 2/5 🟡
