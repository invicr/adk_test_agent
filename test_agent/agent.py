# agent.py

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from datetime import datetime
import os
import requests

# ---------------------
# 🔧 Tavily API 설정
# ---------------------
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_API_URL = "https://api.tavily.com/search"

def search_web(query: str) -> dict:
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TAVILY_API_KEY}"
        }
        payload = {
            "query": query,
            "search_depth": "advanced",
            "include_answer": True,
            "include_raw_content": True,
            "max_results": 5,
        }
        response = requests.post(TAVILY_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        results = response.json()

        formatted_results = {
            "summary": results.get("answer", ""),
            "results": [
                {
                    "title": r.get("title", "제목 없음"),
                    "url": r.get("url", ""),
                    "content": r.get("content", "")[:300],
                    "published_date": r.get("published_date", "날짜 정보 없음")
                } for r in results.get("results", [])
            ]
        }
        return {
            "query": query,
            "summary": formatted_results["summary"],
            "articles": formatted_results["results"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"error": str(e)}

# ---------------------
# 🔍 검색 에이전트
# ---------------------
search_agent = LlmAgent(
    model=LiteLlm(model="openai/gpt-4"),
    name="SearchAgent",
    description="Tavily를 사용하여 웹에서 정보를 검색합니다.",
    instruction="""
state["query"]에서 검색어를 읽고 search_web(query)를 호출하세요.
결과는 state["search_result"]에 저장하세요.
""",
    tools=[search_web]
)

# ---------------------
# 📝 보고서 작성 에이전트
# ---------------------
report_agent = LlmAgent(
    model=LiteLlm(model="openai/gpt-4"),
    name="ReportAgent",
    description="검색 결과를 보고서 형식으로 정리합니다.",
    instruction="""
state["search_result"]의 내용을 기반으로 다음과 같은 형식으로 보고서를 작성하세요:

📌 검색어: [query]
🕒 검색 시간: [timestamp]

📄 요약:
[summary]

🔍 주요 기사:
1. [제목] - [내용 일부 요약]
   출처: [URL]
2. ...
"""
)

# ---------------------
# ▶️ 시퀀셜 파이프라인 정의
# ---------------------
search_and_report_pipeline = SequentialAgent(
    name="SearchAndReport",
    description="Tavily 검색 후 보고서를 작성하는 파이프라인입니다.",
    sub_agents=[search_agent, report_agent]
)

# ---------------------
# 🚀 ADK Web에서 실행될 최상위 에이전트
# ---------------------
root_agent = search_and_report_pipeline
