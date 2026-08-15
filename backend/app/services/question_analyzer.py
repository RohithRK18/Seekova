import re
from typing import Dict, Any, List

class QuestionAnalyzer:
    """
    Production-Grade Question Understanding Engine for SECONDLYBRAIN.
    Classifies every incoming query into structured metadata:
    - Intent (location_overview, mind_map, timeline, calculation, comparison, troubleshooting, coding, explanation, definition, current_info)
    - Domain (Geography, Technology, Programming, Science, History, Culture, Business, Education, Health, Travel, General)
    - Output Type (mindmap, timeline, comparison_table, code_block, location_guide, calculation_card, structured_explanation)
    - Tool Requirements (requires_web, requires_calc, requires_mindmap, requires_timeline, requires_code)
    """

    INTENT_RULES = [
        ("mind_map", ["mind map", "mindmap", "concept map", "brainstorm map"], "mindmap"),
        ("timeline", ["timeline", "chronology", "history of", "evolution of", "milestones"], "timeline"),
        ("calculation", ["calculate", "math", "sum", "multiply", "percentage", "compound interest", "unit conversion", "+", "*", "/"], "calculation_card"),
        ("comparison", ["vs", "versus", "difference", "compare", "which is better"], "comparison_table"),
        ("troubleshooting", ["error", "exception", "failing", "fix", "issue", "bug", "why is my", "500", "404"], "troubleshooting_guide"),
        ("coding", ["write code", "python code", "java code", "binary search", "rest api", "function", "script"], "code_block"),
        ("location_overview", ["tell me about", "where is", "capital of", "visit", "city", "chennai", "madurai", "coimbatore", "delhi", "mumbai", "india", "japan", "rome"], "location_guide"),
        ("current_info", ["latest", "today", "current", "recently", "now", "newest", "2026", "2025", "price", "version", "news"], "structured_explanation"),
    ]

    DOMAINS = {
        "Geography & Travel": ["chennai", "madurai", "coimbatore", "mumbai", "delhi", "india", "himalayas", "climate", "monsoon", "city", "capital", "country", "river", "tourism"],
        "Technology": ["ai", "genai", "artificial intelligence", "kubernetes", "kafka", "graphql", "rest", "cloud", "docker", "microservices", "pubsub", "transformer", "llm", "neural network"],
        "Programming": ["java", "python", "javascript", "react", "nullpointerexception", "garbage collection", "recursion", "oop", "algorithm", "binary search", "sql", "code", "c++"],
        "Science": ["photosynthesis", "quantum", "relativity", "immune system", "physics", "biology", "chemistry", "dna", "atom", "space", "astronomy"],
        "History": ["roman empire", "world war", "industrial revolution", "civilization", "empire", "ancient", "dynasty", "history"],
        "Culture": ["diwali", "tea culture", "tradition", "festival", "culture", "heritage", "art", "music", "temple"],
        "Business & Economics": ["inflation", "stock market", "startup valuation", "economics", "finance", "gdp", "business", "market"],
    }

    def analyze(self, query: str) -> Dict[str, Any]:
        q_clean = query.strip()
        q_lower = q_clean.lower()
        words = re.findall(r'\b\w+\b', q_lower)

        # 1. Detect Intent & Output Type
        detected_intent = "explanation"
        output_type = "structured_explanation"
        
        for intent_key, keywords, out_fmt in self.INTENT_RULES:
            if any(kw in q_lower for kw in keywords):
                detected_intent = intent_key
                output_type = out_fmt
                break

        # 2. Detect Domain
        detected_domain = "General Knowledge"
        max_matches = 0
        for domain, keywords in self.DOMAINS.items():
            matches = sum(1 for kw in keywords if kw in q_lower)
            if matches > max_matches:
                max_matches = matches
                detected_domain = domain

        # 3. Tool Selection Flags
        requires_web = any(w in q_lower for w in ["latest", "current", "today", "2026", "2025", "news", "version", "price"])
        requires_calc = detected_intent == "calculation" or any(char in q_clean for char in ["+", "*", "/"])
        requires_mindmap = output_type == "mindmap"
        requires_timeline = output_type == "timeline"
        requires_code = output_type == "code_block" or "code" in q_lower

        return {
            "query": q_clean,
            "intent": detected_intent,
            "domain": detected_domain,
            "output_type": output_type,
            "complexity": "complex" if len(words) > 8 or detected_intent in ["mind_map", "timeline", "comparison"] else "standard",
            "min_target_words": 150 if detected_intent != "calculation" else 40,
            "tools": {
                "requires_web": requires_web,
                "requires_calc": requires_calc,
                "requires_mindmap": requires_mindmap,
                "requires_timeline": requires_timeline,
                "requires_code": requires_code
            }
        }

question_analyzer = QuestionAnalyzer()
