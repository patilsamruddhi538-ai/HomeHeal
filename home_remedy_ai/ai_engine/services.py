"""AI engine for generating personalized home remedy recommendations."""

import json
import re
from urllib import error, request

from django.conf import settings


INGREDIENT_DB = {
    "honey": {
        "quantity": "2 tsp",
        "aliases": ["honey"],
        "tags": {"antibacterial", "hydrating", "healing"},
        "benefits": ["helps reduce bacterial growth", "supports skin repair"],
        "compounds": ["enzymes", "flavonoids"],
    },
    "lemon": {
        "quantity": "1 tsp diluted juice",
        "aliases": ["lemon", "nimbu"],
        "tags": {"brightening", "astringent", "oil-control"},
        "benefits": ["improves dullness", "helps reduce excess oil"],
        "compounds": ["citric acid", "vitamin C"],
    },
    "turmeric": {
        "quantity": "1/4 tsp",
        "aliases": ["turmeric", "haldi"],
        "tags": {"anti-inflammatory", "antibacterial", "brightening"},
        "benefits": ["calms redness", "supports blemish recovery"],
        "compounds": ["curcumin"],
    },
    "yogurt": {
        "quantity": "1 tbsp",
        "aliases": ["yogurt", "curd", "dahi"],
        "tags": {"hydrating", "gentle-exfoliation", "soothing"},
        "benefits": ["softens rough texture", "provides mild exfoliation"],
        "compounds": ["lactic acid", "probiotics"],
    },
    "aloe vera": {
        "quantity": "1 tbsp gel",
        "aliases": ["aloe vera", "aloe"],
        "tags": {"soothing", "hydrating", "healing"},
        "benefits": ["cools irritation", "supports moisture balance"],
        "compounds": ["polysaccharides", "salicylic acid (trace)"],
    },
    "coconut oil": {
        "quantity": "1 tsp",
        "aliases": ["coconut oil", "nariyal tel"],
        "tags": {"hydrating", "barrier-repair", "hair-nourishing"},
        "benefits": ["reduces dryness", "improves hair softness"],
        "compounds": ["lauric acid", "medium-chain fatty acids"],
    },
    "olive oil": {
        "quantity": "1 tsp",
        "aliases": ["olive oil"],
        "tags": {"hydrating", "barrier-repair", "antioxidant"},
        "benefits": ["supports skin barrier", "nourishes dry hair"],
        "compounds": ["oleic acid", "polyphenols"],
    },
    "oatmeal": {
        "quantity": "1 tbsp ground",
        "aliases": ["oatmeal", "oats"],
        "tags": {"soothing", "anti-inflammatory", "gentle-cleansing"},
        "benefits": ["reduces itch", "calms sensitive skin"],
        "compounds": ["beta-glucans", "avenanthramides"],
    },
    "cucumber": {
        "quantity": "2 tbsp pulp",
        "aliases": ["cucumber", "kheera"],
        "tags": {"cooling", "hydrating", "de-puffing"},
        "benefits": ["refreshes tired skin", "reduces puffiness"],
        "compounds": ["silica", "vitamin K"],
    },
    "green tea": {
        "quantity": "2 tbsp brewed",
        "aliases": ["green tea"],
        "tags": {"antioxidant", "anti-inflammatory", "oil-control"},
        "benefits": ["calms acne-prone skin", "reduces oxidative stress"],
        "compounds": ["catechins", "EGCG"],
    },
    "milk": {
        "quantity": "1 tbsp",
        "aliases": ["milk"],
        "tags": {"hydrating", "gentle-exfoliation", "brightening"},
        "benefits": ["softens skin", "improves rough patches"],
        "compounds": ["lactic acid", "milk proteins"],
    },
    "banana": {
        "quantity": "2 tbsp mashed",
        "aliases": ["banana", "kela"],
        "tags": {"hydrating", "hair-nourishing", "barrier-repair"},
        "benefits": ["improves moisture retention", "adds softness"],
        "compounds": ["potassium", "vitamin B6"],
    },
    "avocado": {
        "quantity": "2 tbsp mashed",
        "aliases": ["avocado"],
        "tags": {"hydrating", "barrier-repair", "hair-nourishing"},
        "benefits": ["supports dry skin", "improves hair texture"],
        "compounds": ["vitamin E", "oleic acid"],
    },
    "tea tree oil": {
        "quantity": "1 drop (diluted)",
        "aliases": ["tea tree oil", "tea tree"],
        "tags": {"antibacterial", "antifungal", "acne"},
        "benefits": ["helps reduce acne bacteria", "supports scalp hygiene"],
        "compounds": ["terpinen-4-ol"],
    },
    "apple cider vinegar": {
        "quantity": "1 tsp diluted in 3 tsp water",
        "aliases": ["apple cider vinegar", "acv", "vinegar"],
        "tags": {"pH-balance", "clarifying", "oil-control"},
        "benefits": ["helps balance scalp/skin pH", "reduces buildup"],
        "compounds": ["acetic acid"],
    },
    "fenugreek": {
        "quantity": "1 tbsp soaked paste",
        "aliases": ["fenugreek", "methi"],
        "tags": {"hair-fall", "anti-inflammatory", "scalp-care"},
        "benefits": ["supports weak roots", "helps reduce flaking"],
        "compounds": ["nicotinic acid", "saponins"],
    },
}


PROBLEM_PROFILES = [
    {
        "name": "Acne / Pimples",
        "keywords": ["acne", "pimple", "breakout", "blackhead", "whitehead"],
        "target_tags": {"antibacterial", "anti-inflammatory", "oil-control", "acne"},
        "usage": "Apply 2 to 3 times weekly in the evening. Use as a thin layer on affected areas, rinse after 15 minutes.",
        "goal": "control excess oil, calm active inflammation, and reduce future breakouts",
    },
    {
        "name": "Dry Skin",
        "keywords": ["dry", "dehydrated", "flaky", "rough", "tight skin"],
        "target_tags": {"hydrating", "barrier-repair", "soothing"},
        "usage": "Use once daily or every alternate day on damp skin. Leave for 20 minutes and follow with moisturizer.",
        "goal": "restore hydration and repair the skin barrier",
    },
    {
        "name": "Dandruff / Scalp Irritation",
        "keywords": ["dandruff", "scalp", "itchy scalp", "flakes"],
        "target_tags": {"antifungal", "anti-inflammatory", "scalp-care", "pH-balance"},
        "usage": "Apply on scalp roots 2 times weekly before hair wash. Keep for 25 to 30 minutes.",
        "goal": "reduce flakes, calm scalp irritation, and support scalp hygiene",
    },
    {
        "name": "Hair Fall / Weak Hair",
        "keywords": ["hair fall", "hair loss", "weak hair", "thinning"],
        "target_tags": {"hair-fall", "hair-nourishing", "anti-inflammatory", "scalp-care"},
        "usage": "Massage into scalp and hair lengths 2 to 3 times weekly. Leave for 30 minutes before washing.",
        "goal": "support scalp health and strengthen hair roots",
    },
    {
        "name": "Pigmentation / Uneven Tone",
        "keywords": ["pigmentation", "dark spot", "tan", "dull", "uneven tone"],
        "target_tags": {"brightening", "gentle-exfoliation", "antioxidant"},
        "usage": "Use 2 times weekly at night. Keep contact time short at first (8 to 10 minutes) and increase gradually.",
        "goal": "improve tone and reduce surface dullness",
    },
]


def generate_ai_remedy(problem_description, available_ingredients, user):
    """Generate structured remedy payload and return JSON text for storage."""
    sections = generate_ai_remedy_sections(problem_description, available_ingredients, user)
    return json.dumps(sections)


def parse_ai_remedy_payload(payload_text):
    """Convert stored remedy payload to a normalized section dictionary for templates."""
    if not payload_text:
        return _legacy_payload_to_sections("")

    try:
        parsed = json.loads(payload_text)
    except (TypeError, json.JSONDecodeError):
        return _legacy_payload_to_sections(payload_text)

    if not isinstance(parsed, dict):
        return _legacy_payload_to_sections(payload_text)

    return _normalize_sections(parsed)


def generate_ai_remedy_sections(problem_description, available_ingredients, user):
    """Generate consultation in a section-wise format."""
    profile = _extract_profile(user)
    ingredient_names = _parse_ingredients(available_ingredients)

    ai_payload, failure_reason = _generate_with_openai(problem_description, ingredient_names, profile)
    if ai_payload:
        ai_payload["generation_source"] = "openai"
        return _normalize_sections(ai_payload)

    # Fall back to local rule-based generation so users still get usable guidance.
    fallback_payload = _generate_rule_based(problem_description, ingredient_names, profile)
    fallback_payload["generation_source"] = "rule_based"
    fallback_payload["failure_reason"] = failure_reason or "unknown"
    return _normalize_sections(fallback_payload)


def _extract_profile(user):
    profile = getattr(user, "profile", None)
    return {
        "name": user.first_name or user.username,
        "skin_type": getattr(profile, "skin_type", "") or "normal",
        "hair_type": getattr(profile, "hair_type", "") or "normal",
        "allergies": getattr(profile, "allergies", "") or "none",
    }


def _parse_ingredients(available_ingredients):
    if not available_ingredients:
        return []

    parts = re.split(r"[,\n;]+", available_ingredients.lower())
    cleaned = []
    for item in parts:
        token = re.sub(r"\s+", " ", item.strip())
        if token and token not in cleaned:
            cleaned.append(token)
    return cleaned


def _build_unavailable_sections(problem_description, ingredient_names, failure_reason):
    reason_text = {
        "missing_api_key": "OPENAI_API_KEY is not configured in environment variables.",
        "http_error": "AI API request failed due to an HTTP/network issue.",
        "invalid_response": "AI API returned an unexpected response format.",
    }.get(failure_reason, "AI generation is currently unavailable.")

    ingredients_line = ", ".join(ingredient_names) if ingredient_names else "Not provided"

    return _normalize_sections(
        {
            "title": "Real AI Response Unavailable",
            "description": "This consultation is configured for live AI generation only.",
            "matched_problem": "Pending AI Analysis",
            "ingredients": [f"Provided by user: {ingredients_line}"],
            "instructions": [
                "Set OPENAI_API_KEY in your environment.",
                "Restart the Django server after setting environment variables.",
                "Submit the consultation again to get a real model response.",
            ],
            "usage": "No generated routine available until the live AI model responds.",
            "benefits": [
                "Ensures output is generated by a real AI model.",
                "Prevents static or pre-fed fallback responses.",
            ],
            "chemicals": "",
            "reactions": "",
            "importance": f"Reason: {reason_text}",
            "precautions": [
                "For severe symptoms, consult a healthcare professional.",
                "Do not rely on incomplete guidance when AI is unavailable.",
            ],
            "generation_source": "unavailable",
            "failure_reason": failure_reason or "unknown",
            "problem_echo": problem_description,
        }
    )


def _detect_problem_profile(problem_description):
    text = (problem_description or "").lower()
    best = None
    best_score = 0

    for profile in PROBLEM_PROFILES:
        score = sum(1 for keyword in profile["keywords"] if keyword in text)
        if score > best_score:
            best = profile
            best_score = score

    return best


def _resolve_ingredient(token):
    for ingredient_name, data in INGREDIENT_DB.items():
        for alias in data["aliases"]:
            if alias in token:
                return ingredient_name
    return None


def _pick_ingredients(ingredient_tokens, target_tags):
    picks = []
    used = set()

    for token in ingredient_tokens:
        ingredient_name = _resolve_ingredient(token)
        if not ingredient_name or ingredient_name in used:
            continue

        tags = INGREDIENT_DB[ingredient_name]["tags"]
        score = len(tags.intersection(target_tags))
        if score > 0:
            picks.append((score, ingredient_name))
            used.add(ingredient_name)

    picks.sort(reverse=True)
    selected = [name for _, name in picks[:4]]

    if not selected:
        for token in ingredient_tokens[:3]:
            selected.append(token.title())

    if not selected:
        selected = ["Plain yogurt", "Aloe vera gel"]

    return selected


def _generate_rule_based(problem_description, ingredient_tokens, profile):
    matched_problem = _detect_problem_profile(problem_description)
    target_tags = matched_problem["target_tags"] if matched_problem else {"hydrating", "soothing"}
    selected = _pick_ingredients(ingredient_tokens, target_tags)

    structured_ingredients = []
    all_compounds = []
    all_benefits = []

    for item in selected:
        key = item.lower()
        if key in INGREDIENT_DB:
            db_item = INGREDIENT_DB[key]
            structured_ingredients.append(
                f"{item.title()} - {db_item['quantity']} ({', '.join(sorted(db_item['tags']))})"
            )
            all_compounds.extend(db_item["compounds"])
            all_benefits.extend(db_item["benefits"])
        else:
            structured_ingredients.append(f"{item} - use 1 to 2 tsp based on consistency")

    base_goal = matched_problem["goal"] if matched_problem else "target your reported concern gently"
    usage_text = (
        matched_problem["usage"]
        if matched_problem
        else "Apply 2 times weekly on clean skin or scalp and rinse after 15 to 20 minutes."
    )

    instructions = [
        "Clean a mixing bowl and wash hands before preparation.",
        f"Add {', '.join(item.split(' - ')[0] for item in structured_ingredients)} into the bowl.",
        "Mix until a smooth, spreadable paste forms. Add a few drops of water only if required.",
        "Patch test on the inner arm for 24 hours before full application.",
        "Apply a thin and even layer on the target area.",
        "Rinse gently with lukewarm water and pat dry.",
    ]

    benefits = _dedupe_list(all_benefits)
    if not benefits:
        benefits = [
            "uses readily available home ingredients",
            "offers a low-cost routine you can repeat consistently",
        ]

    benefits = [f"{benefit.capitalize()}." for benefit in benefits[:6]]
    benefits.insert(0, f"Designed to {base_goal}.")

    chemicals = ", ".join(_dedupe_list(all_compounds)[:8]) or "Natural plant acids, antioxidants, and soothing compounds"
    reactions = (
        "These compounds support barrier repair, reduce inflammation, and improve microbial balance when used consistently."
    )
    importance = (
        f"This plan is tailored for {profile['name']} using available ingredients and profile context "
        f"(skin type: {profile['skin_type']}, hair type: {profile['hair_type']})."
    )

    precautions = [
        "Do not use on broken or infected skin.",
        "Avoid eye and lip contact.",
        "Stop use immediately if burning, rash, or swelling occurs.",
        "Use sunscreen during daytime when using acidic ingredients.",
        f"Known allergies noted: {profile['allergies']}. Exclude matching ingredients.",
    ]

    if any("lemon" in line.lower() or "vinegar" in line.lower() for line in structured_ingredients):
        precautions.append("Do not exceed recommended contact time for acidic ingredients.")

    return {
        "title": "Personalized AI Remedy Plan",
        "description": "Generated from your problem description, available ingredients, and profile details.",
        "matched_problem": matched_problem["name"] if matched_problem else "General Care",
        "ingredients": structured_ingredients,
        "instructions": instructions,
        "usage": usage_text,
        "benefits": benefits,
        "chemicals": chemicals,
        "reactions": reactions,
        "importance": importance,
        "precautions": precautions,
    }


def _generate_with_openai(problem_description, ingredient_names, profile):
    api_key = getattr(settings, "OPENAI_API_KEY", "").strip()
    if not api_key:
        return None, "missing_api_key"

    model = getattr(settings, "OPENAI_MODEL", "gpt-4o-mini")
    api_url = getattr(settings, "OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")
    timeout = int(getattr(settings, "OPENAI_TIMEOUT", 25) or 25)
    payload = {
        "model": model,
        "temperature": 0.4,
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a careful home remedy assistant. Respond ONLY as valid JSON with keys: "
                    "title, description, matched_problem, ingredients (array), instructions (array), usage, "
                    "benefits (array), chemicals, reactions, importance, precautions (array). "
                    "Avoid medical diagnosis and include safe caution advice."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "problem_description": problem_description,
                        "available_ingredients": ingredient_names,
                        "profile": profile,
                    }
                ),
            },
        ],
    }

    req = request.Request(
        url=api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        if exc.code in {401, 403}:
            return None, "invalid_api_key"
        if exc.code == 429:
            return None, "rate_limited"
        return None, "http_error"
    except (error.URLError, TimeoutError):
        return None, "network_error"
    except json.JSONDecodeError:
        return None, "http_error"

    try:
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        if isinstance(parsed, dict):
            return parsed, None
        return None, "invalid_response"
    except (KeyError, IndexError, TypeError, json.JSONDecodeError):
        return None, "invalid_response"


def _normalize_sections(data):
    return {
        "title": str(data.get("title") or "Personalized AI Remedy Plan"),
        "description": str(data.get("description") or "Custom recommendation generated for your inputs."),
        "matched_problem": str(data.get("matched_problem") or "General Care"),
        "ingredients": _safe_list(data.get("ingredients")),
        "instructions": _safe_list(data.get("instructions")),
        "usage": str(data.get("usage") or "Use as advised by the live AI consultation."),
        "benefits": _safe_list(data.get("benefits")),
        "chemicals": str(data.get("chemicals") or ""),
        "reactions": str(data.get("reactions") or ""),
        "importance": str(data.get("importance") or ""),
        "precautions": _safe_list(data.get("precautions")),
        "generation_source": str(data.get("generation_source") or "unavailable"),
        "failure_reason": str(data.get("failure_reason") or ""),
        "problem_echo": str(data.get("problem_echo") or ""),
    }


def _safe_list(value):
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        lines = [item.strip("-• ").strip() for item in value.splitlines() if item.strip()]
        return lines
    return []


def _dedupe_list(items):
    seen = set()
    result = []
    for item in items:
        key = item.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item.strip())
    return result


def _legacy_payload_to_sections(payload_text):
    lines = [line.strip() for line in str(payload_text).splitlines() if line.strip()]
    return {
        "title": "Personalized AI Remedy Plan",
        "description": "Legacy consultation format.",
        "matched_problem": "General Care",
        "ingredients": [],
        "instructions": [],
        "usage": "",
        "benefits": [],
        "chemicals": "",
        "reactions": "",
        "importance": "",
        "precautions": [],
        "generation_source": "legacy",
        "legacy_text": "\n".join(lines),
    }
