import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"

def extract_json(text: str) -> str:
    """
    Extract JSON object from messy LLM output
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def analyze_contract(text: str) -> dict:
    prompt = f"""
You are a legal contract analysis assistant.

Return ONLY valid JSON. No explanation, no markdown.

Schema:
{{
  "summary": "3-4 line business summary",
  "risk_level": "Low | Medium | High",
  "key_issues": ["issue 1"],
  "clauses": {{
    "termination": "present/missing/weak",
    "liability": "limited/unlimited/unclear",
    "payment_terms": "clear/unclear/missing",
    "confidentiality": "present/missing"
  }}
}}

Contract:
{text}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        print("OLLAMA RAW RESPONSE:", data)

        raw_output = data.get("response", "").strip()

        if not raw_output:
            raise ValueError("Empty response from Ollama")

        # Remove markdown
        raw_output = raw_output.replace("```json", "").replace("```", "").strip()

        # Extract clean JSON
        raw_output = extract_json(raw_output)

        # Parse JSON
        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError as e:
            print("❌ JSON parsing failed:", e)

            return {
                "summary": raw_output[:300],
                "risk_level": "Unknown",
                "key_issues": [],
                "clauses": {}
            }

        # 🔥 Enforce schema (VERY IMPORTANT)
        return {
            "summary": parsed.get("summary", ""),
            "risk_level": parsed.get("risk_level", "Unknown"),
            "key_issues": parsed.get("key_issues", []),
            "clauses": parsed.get("clauses", {})
        }

    except Exception as e:
        print("Ollama error:", e)

        return {
            "summary": "Error analyzing contract",
            "risk_level": "Unknown",
            "key_issues": [],
            "clauses": {}
        }