def build_prompt(cv_text: str) -> str:
    return f"""
You are a senior technical recruiter with 10+ years of experience.

You MUST return STRICT JSON only.
No explanation. No markdown. No extra text.
Return one single JSON object only.
Do not wrap JSON in code fences.
All keys must be present.

Analyze the resume below across 10 parameters.

RESUME:
{cv_text}

SCORING RULES:
- Be brutally honest
- Most student resumes score between 35-55
- Only give 70+ if genuinely strong

RETURN EXACT JSON:

{{
  "overall_score": <integer 0-100>,
  "grade": "<A/B/C/D/F>",
  "overall_verdict": "<2-3 sentence honest summary>",
  "parameters": [
    {{
      "name": "Contact Information Completeness",
      "score": <0-10>,
      "weight": 5,
      "feedback": "<specific feedback>",
      "status": "<good/improve/critical>"
    }},
    {{
      "name": "Professional Summary",
      "score": <0-10>,
      "weight": 10,
      "feedback": "<specific feedback>",
      "status": "<good/improve/critical>"
    }},
    {{
      "name": "Skills Section",
      "score": <0-10>,
      "weight": 10,
      "feedback": "<specific feedback>",
      "status": "<good/improve/critical>"
    }},
    {{
      "name": "Projects & Experience",
      "score": <0-10>,
      "weight": 20,
      "feedback": "<specific feedback>",
      "status": "<good/improve/critical>"
    }},
    {{
      "name": "ATS Keywords",
      "score": <0-10>,
      "weight": 15,
      "feedback": "<specific feedback>",
      "status": "<good/improve/critical>"
    }},
    {{
      "name": "Education",
      "score": <0-10>,
      "weight": 5,
      "feedback": "<specific feedback>",
      "status": "<good/improve/critical>"
    }},
    {{
      "name": "Formatting & Clarity",
      "score": <0-10>,
      "weight": 10,
      "feedback": "<specific feedback>",
      "status": "<good/improve/critical>"
    }},
    {{
      "name": "Resume Length",
      "score": <0-10>,
      "weight": 5,
      "feedback": "<specific feedback>",
      "status": "<good/improve/critical>"
    }},
    {{
      "name": "Achievements vs Responsibilities",
      "score": <0-10>,
      "weight": 10,
      "feedback": "<specific feedback>",
      "status": "<good/improve/critical>"
    }},
    {{
      "name": "Overall Professional Impression",
      "score": <0-10>,
      "weight": 10,
      "feedback": "<specific feedback>",
      "status": "<good/improve/critical>"
    }}
  ],
  "top_3_critical_issues": [
    "<issue 1>",
    "<issue 2>",
    "<issue 3>"
  ],
  "ats_keywords_missing": [
    "<keyword 1>",
    "<keyword 2>",
    "<keyword 3>"
  ],
  "rewritten_sections": {{
    "summary": "<improved summary>",
    "one_weak_bullet_rewrite": "<original vs improved>"
  }}
}}
"""
