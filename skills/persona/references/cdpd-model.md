# Cross-Domain Persona Decision (CDPD) Model

## 용어 정의

### Constants

| 기호 | 이름 | 의미 | 실험값 |
|:----:|:-----|:-----|:------:|
| **Φ_s** | *Singular Quality Baseline* | S=0 단일 페르소나 품질 | 0.85 |
| **Φ_m** | *Multi Quality Baseline* | S=0 멀티 페르소나 품질 | 0.90 |
| **α** | *Alpha — Singular Decay Rate* | S 1↑ 시 단일 품질 감소 | 0.125 |
| **β** | *Beta — Multi Boost Rate* | S 1↑ 시 멀티 품질 증가 | 0.025 |
| **Γ_base** | *Gamma — Multi Base Overhead* | 멀티 로딩 고정 비용 | 43,122 tok |
| **k** | *Kappa — Token Normalizer* | C_single(0) 기준 | 12,764 tok |
| **η** | *Eta — Quality-Cost Tradeoff* | 품질 대비 비용 민감도 | 0.3 (설정 가능) |
| **T** | *Theta — Decision Threshold* | 단일↔멀티 전환 임계값 | ≈1.18, ceil=2 |

### Variables

| 기호 | 의미 |
|:----:|:------|
| **S** | *Sigma* — 태스크 키워드 중 메인 카테고리 밖 단어 수 |
| **ψ** | *Psi* — 지연시간 민감도 |
| **Ω** | *Omega* — 요구 품질 수준 |

### Functions

| 함수 | 정의 |
|:-----|:------|
| Q_single(S) | Φ_s − α·S |
| Q_multi(S) | Φ_m + β·S |
| U(S, η) | Q(S) − η·C(S)/k |

## 임계값 방정식

U_multi(T) = U_single(T):

```
(Φ_m + β·T) − η·(k + Γ_base + 9,293·T)/k = (Φ_s − α·T) − η·(k + 37,517·T)/k
```

정리 (η=0.3):

```
0.05 + 0.15T − 0.3·43,122/12,764 + 0.3·28,224·T/12,764 = 0
0.813T = 0.963
T ≈ 1.18
```

## 증명 성질

| S | ΔU | 최적 |
|:-:|:--:|:----:|
| 0 | −0.96 | 단일 |
| 1 | −0.15 | 단일 |
| 2 | +0.67 | 멀티 |
| 3+ | +2.43+ | 멀티 (clamp 3) |

저지연·고품질 시나리오에서도 T 유지 (ψ-Ω 상쇄). 1토큰 정밀도로 S=1과 S=2 구분 가능 (ΔU 차이 0.82).

## 실험 기반

1. S=0: 서버리스 설명 — 단일 24초/12K vs 멀티 61초/56K. ΔU=-0.96
2. S=2: 논문 작성 — 순차 297초/163K vs 멀티 182초/74K. ΔU=+2.43

## 교정 프로토콜

새 모델 사용 시 4개 실험 재실행:
1. S=0 single → Φ_s, k
2. S=0 multi → Φ_m, Γ_base
3. S=2 single → α
4. S=2 multi → β
→ T 재계산
