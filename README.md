# 🔎 Tavily 검색 및 보고서 생성 에이전트 (ADK Web용)

이 프로젝트는 Google의 Agent Development Kit (ADK)를 기반으로, Tavily API를 사용해 웹 검색을 수행하고 그 결과를 요약 보고서 형태로 생성하는 에이전트를 제공합니다.  
ADK Web UI를 통해 자연어로 검색어를 입력하면, 두 개의 에이전트(`SearchAgent`와 `ReportAgent`)가 순차적으로 실행됩니다.

---

## 📦 설치 환경

Python 환경 준비 (권장: 3.9 ~ 3.10)

```bash
python -m venv adk-env
source adk-env/bin/activate  # or .\adk-env\Scripts\activate on Windows

pip install python-dotenv

adk web --app my_agent
