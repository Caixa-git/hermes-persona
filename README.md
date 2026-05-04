<p align="center">
  <img src="https://img.shields.io/badge/작업에_맞는_전문가를_자동으로-배정합니다-8A2BE2?style=flat-square" alt="subtitle">
</p>

<p align="center">
  <samp>
    <big><strong>🎭 Hermes Persona</strong></big><br>
    <br>
    <sub>
      칸반에 할당된 모든 작업에<br>
      가장 적합한 전문가 페르소나를 자동 선택합니다
    </sub>
  </samp>
</p>

<p align="center">
  <a href="https://github.com/NousResearch/hermes-agent">
    <img src="https://img.shields.io/badge/runs_on-Hermes_Agent-8A2BE2?style=flat-square&logo=robot" alt="Hermes Agent">
  </a>
  <a href="https://github.com/msitarzewski/agency-agents">
    <img src="https://img.shields.io/badge/uses-agency_agents-FF6B6B?style=flat-square" alt="Agency Agents">
  </a>
  <img src="https://img.shields.io/badge/172_전문가_역할-FFD700?style=flat-square" alt="172 experts">
  <img src="https://img.shields.io/badge/설치_1초-grey?style=flat-square" alt="install">
</p>

<br>

---

안녕하세요. **Hermes Persona**입니다.

Hermes Agent가 작업을 처리할 때, 그 작업에 가장 어울리는 전문가의 성격과 업무 방식을 자동으로 적용해주는 시스템입니다.

172명의 전문가 중에서 작업 내용을 분석해 가장 적합한 한 명을 골라, 그 전문가처럼 일하게 됩니다.

<br>

## 📖 이런 겁니다

Hermes Agent에 작업을 요청하면, 이 시스템이 다음과 같이 반응합니다.

| 작업 내용 | 선택되는 전문가 |
|----------|---------------|
| 온라인 쇼핑몰 제작 | 🏗️ 건축가 (Backend Architect) |
| 대시보드 화면 디자인 | 🎨 디자이너 (Frontend Developer) |
| 서버 보안 점검 | 🔒 보안 전문가 (Security Engineer) |
| 앱 출시 준비 | 🚀 운영 전문가 (DevOps Automator) |
| 데이터베이스 속도 개선 | 🗄️ 데이터 최적화 전문가 (Database Optimizer) |
| 모바일 앱 개발 | 📱 앱 개발자 (Mobile App Builder) |

전문가 한 명 한 명은 각자의 작업 방식, 원칙, 체크리스트를 가지고 있습니다. 작업을 할당받으면 그 전문가의 방식으로 일합니다.

<br>

## 🔄 어떻게 작동하나요

작업이 할당되면 아래 과정이 자동으로 실행됩니다.

```
작업 할당 → 작업 내용 분석 → 172명의 전문가 검토
    → 가장 적합한 전문가 선정
    → 그 전문가의 방식으로 작업 시작
    → "지금부터 🏗️ 건축가로서 작업합니다" 기록
```

모든 전문가 정보는 원격지에서 실시간으로 불러옵니다. 내 컴퓨터에 따로 저장하거나 관리할 것이 없습니다.

<br>

## 📦 설치 방법

Hermes Agent가 설치된 컴퓨터에서 아래 한 줄을 복사해 터미널에 붙여넣고 Enter를 누르면 됩니다.

```bash
bash <(curl -sSL https://raw.githubusercontent.com/Caixa-git/hermes-persona/main/install.sh)
```

설치가 끝나면 별도 설정 없이 바로 사용할 수 있습니다.

> **Hermes Agent 설치**가 아직이라면<br>
> ➡ https://github.com/NousResearch/hermes-agent

<br>

## 🗺️ 앞으로의 계획

- [x] 기본 전문가 자동 선택 — 172개 역할, 조건 없음, 설치 즉시 작동
- [x] 이모지 표시 — 선택된 전문가를 칸반에서 바로 확인 가능
- [ ] **똑똑한 역할 선택** — 여러 기준을 종합해 더 정확하게 전문가를 골라냅니다

<br>

## 🙏 만든 사람들

| 프로젝트 | 만든 이 | 설명 |
|----------|--------|------|
| [agency-agents](https://github.com/msitarzewski/agency-agents) | msitarzewski | 15개 분야 172명의 AI 전문가 역할을 정리한 카탈로그 |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Nous Research | AI 에이전트가 작업을 자동으로 처리하는 시스템 |

<br>

---

<p align="center">
  <sub>🎭 Pick your mask. Become the expert.</sub><br>
  <sub>만든 사람 <a href="https://github.com/Caixa-git">Caixa-git</a></sub>
</p>
