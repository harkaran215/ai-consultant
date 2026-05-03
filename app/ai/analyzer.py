import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def analyze_contract(text: str) -> dict:
    prompt = f"""
You are a legal contract analysis assistant.

Your task is to analyze the contract and extract structured information.

Focus ONLY on these clauses:
1. Termination clause
2. Liability clause
3. Payment terms
4. Confidentiality clause

Evaluation rules:
- HIGH risk:
  - Unlimited liability
  - Missing termination clause
  - Unclear or missing payment terms
- MEDIUM risk:
  - One weak or unclear clause
- LOW risk:
  - All clauses present and reasonable

Return STRICT JSON ONLY:

{{
  "summary": "3-4 line business summary",
  "risk_level": "Low | Medium | High",
  "key_issues": [
    "issue 1",
    "issue 2"
  ],
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

        # 🔍 DEBUG (very important)
        print("OLLAMA RAW RESPONSE:", data)

        raw_output = data.get("response", "").strip()

        if not raw_output:
            raise ValueError("Empty response from Ollama")

        # Clean markdown if present
        raw_output = raw_output.replace("```json", "").replace("```", "").strip()

        # Try parsing JSON
        try:
            return json.loads(raw_output)

        except json.JSONDecodeError:
            print("⚠️ JSON parsing failed, returning fallback")

            return {
                "summary": raw_output[:300],
                "risk_level": "Unknown",
                "key_issues": []
            }

    except Exception as e:
        print("Ollama error:", e)

        return {
            "summary": "Error analyzing contract",
            "risk_level": "Unknown",
            "key_issues": []
        }