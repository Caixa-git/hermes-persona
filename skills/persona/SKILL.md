---
name: persona
description: "🎭 자동 페르소나 시스템 — 칸반 워커가 작업 분석 후 172개 전문가 역할 중 최적을 선택합니다"
---

# 🎭 persona — 페르소나 역할 시스템

Hermes Persona가 설치된 환경에서는 이 스킬을 별도로 로드할 필요가 없습니다.

모든 칸반 워커는 KANBAN_GUIDANCE를 통해 자동으로:

1. 작업 분석
2. agency-agents README 조회 (GitHub raw)
3. 최적 역할 선택
4. kanban_heartbeat로 역할 기록
5. 해당 역할의 .md 로드
6. 전문가 모드로 작업

일치하는 역할이 없으면 일반 워커로 동작합니다.

## 참고 URL

- 카탈로그: `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/README.md`
- 역할 파일: `https://raw.githubusercontent.com/msitarzewski/agency-agents/main/{category}/{filename}.md`

## 프로젝트 저장소

https://github.com/Caixa-git/hermes-persona
