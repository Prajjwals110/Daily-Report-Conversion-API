from groq import Groq
from config.settings import GROQ_API_KEY
import json
import re

client = Groq(api_key=GROQ_API_KEY)


def extract_report(text: str):
    prompt = f"""
    Convert this into structured JSON ONLY.

    IMPORTANT RULES:
    - Return ONLY valid JSON
    - Do NOT use ``` or markdown
    - Do NOT add explanation

    Text: {text}

    Output format:
    {{
      "workers": number,
      "delay_hours": number,
      "work_done": string,
      "issues": string or null
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)

    except:
        # 🔥 Remove markdown if present
        content = re.sub(r"```.*?\n", "", content)
        content = content.replace("```", "").strip()

        # 🔥 Extract JSON from text
        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            try:
                return json.loads(match.group())
            except:
                pass

        return {"error": "Invalid JSON", "raw": content}

def generate_summary(text: str):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
                Create a SHORT, practical daily site report.

                Rules:
                - Keep it simple (like a site manager would write)
                - No fancy language
                - No headings like "Recommendations"
                - Just clear info

                Format:
                - Total workers
                - Total delay
                - Work done
                - Issues (if any)

                Data:
                {text}
                """
            }
        ]
    )

    return response.choices[0].message.content.strip()