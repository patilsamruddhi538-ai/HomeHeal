"""
AI Engine for generating personalized home remedy recommendations
"""

def generate_ai_remedy(problem_description, available_ingredients, user):
    """
    Generate AI-powered remedy suggestions based on user's problem and available ingredients
    
    Args:
        problem_description: Description of the health/beauty issue
        available_ingredients: List of products/ingredients available at home
        user: The user requesting the consultation
    
    Returns:
        Formatted remedy suggestion as a string
    """
    
    # Get user profile information for personalization
    profile = user.profile
    skin_type = profile.skin_type if profile.skin_type else "normal"
    allergies = profile.allergies if profile.allergies else "none"
    
    # Create a comprehensive remedy based on common natural ingredients
    remedy_template = f"""
🌿 **Personalized Home Remedy for {user.first_name or user.username}**

**Your Problem:** {problem_description}

**Available Ingredients:** {available_ingredients}

**Your Profile:**
- Skin Type: {skin_type}
- Known Allergies: {allergies}

---

**RECOMMENDED REMEDY:**

Based on your available ingredients and profile, here's a customized natural remedy:

**Ingredients Needed:**
{_generate_ingredient_list(available_ingredients)}

**Preparation Instructions:**
{_generate_instructions(problem_description, available_ingredients)}

**How to Use:**
{_generate_usage(problem_description)}

**Benefits:**
{_generate_benefits(problem_description, available_ingredients)}

**Active Compounds & How They Work:**
{_generate_chemical_info(available_ingredients)}

**Precautions:**
{_generate_precautions(skin_type, allergies)}

**Expected Results:**
You should notice improvements within 1-2 weeks with regular use. If symptoms persist or worsen, please consult a healthcare professional.

**Additional Tips:**
- Patch test on a small area before full application
- Store any leftover mixture in refrigerator for up to 3 days
- Best results when used consistently
"""
    
    return remedy_template


def _generate_ingredient_list(ingredients_str):
    """Generate formatted ingredient list"""
    common_ingredients = {
        'honey': '2 tablespoons organic honey (antibacterial, moisturizing)',
        'lemon': '1 tablespoon fresh lemon juice (vitamin C, brightening)',
        'turmeric': '1 teaspoon turmeric powder (anti-inflammatory)',
        'yogurt': '2 tablespoons plain yogurt (lactic acid, exfoliating)',
        'aloe vera': '2 tablespoons fresh aloe vera gel (soothing, healing)',
        'coconut oil': '1 tablespoon coconut oil (moisturizing, antimicrobial)',
        'olive oil': '1 tablespoon extra virgin olive oil (nourishing)',
        'oatmeal': '2 tablespoons ground oatmeal (soothing, anti-inflammatory)',
        'cucumber': '1/2 cucumber, blended (cooling, hydrating)',
        'egg': '1 egg white (protein, skin tightening)',
        'apple cider vinegar': '1 teaspoon apple cider vinegar (pH balancing)',
        'green tea': '2 tablespoons brewed green tea (antioxidants)',
        'sugar': '2 tablespoons sugar (exfoliating)',
        'milk': '2 tablespoons milk (lactic acid, brightening)',
        'baking soda': '1 teaspoon baking soda (exfoliating, pH balancing)',
        'tea tree oil': '2-3 drops tea tree oil (antibacterial)',
        'banana': '1 ripe banana, mashed (moisturizing, vitamins)',
        'avocado': '1/2 avocado, mashed (nourishing, fatty acids)',
        'potato': '1 small potato, grated (vitamin C, brightening)',
        'rice': '2 tablespoons rice flour (exfoliating, brightening)',
    }
    
    ingredients_lower = ingredients_str.lower()
    selected_ingredients = []
    
    for ingredient, measurement in common_ingredients.items():
        if ingredient in ingredients_lower:
            selected_ingredients.append(f"• {measurement}")
    
    if not selected_ingredients:
        return "• Based on your available items, we'll create a simple mixture"
    
    return "\n".join(selected_ingredients[:5])  # Limit to 5 ingredients


def _generate_instructions(problem, ingredients):
    """Generate step-by-step instructions"""
    instructions = """
1. **Prepare your workspace:** Clean and sanitize a small bowl and mixing spoon
2. **Mix ingredients:** Combine all ingredients in the bowl and mix until smooth and well-blended
3. **Test consistency:** The mixture should be paste-like and easy to apply
4. **Cleanse:** Wash the affected area with lukewarm water and pat dry
5. **Apply:** Gently apply the mixture evenly using clean hands or a brush
6. **Wait:** Leave on for 15-20 minutes, or until it dries
7. **Rinse:** Remove with lukewarm water using gentle circular motions
8. **Moisturize:** Pat dry and apply a light moisturizer if needed
"""
    return instructions


def _generate_usage(problem):
    """Generate usage recommendations"""
    if any(keyword in problem.lower() for keyword in ['acne', 'pimple', 'breakout']):
        return """
• Apply 2-3 times per week, preferably in the evening
• Use as a spot treatment on affected areas
• Can be used all over face if needed
• Best applied after cleansing, before moisturizer
"""
    elif any(keyword in problem.lower() for keyword in ['dry', 'dehydrat', 'flaky']):
        return """
• Use daily or every other day
• Apply to damp skin for better absorption
• Leave on for 20-30 minutes for deep hydration
• Can be used as an overnight treatment
"""
    elif any(keyword in problem.lower() for keyword in ['hair', 'scalp', 'dandruff']):
        return """
• Apply to hair/scalp 2-3 times per week
• Leave on for 30 minutes to 1 hour
• Cover with a shower cap for better penetration
• Rinse thoroughly with lukewarm water and mild shampoo
"""
    else:
        return """
• Use 2-3 times per week for best results
• Apply to clean, dry skin
• Leave on for 15-20 minutes
• Rinse with lukewarm water
"""


def _generate_benefits(problem, ingredients):
    """Generate benefit list based on ingredients"""
    benefits = [
        "✓ Natural and chemical-free alternative",
        "✓ Cost-effective using household ingredients",
        "✓ Gentle on skin with minimal side effects",
        "✓ Provides essential nutrients and vitamins",
        "✓ Suitable for regular use",
        "✓ Improves overall skin/hair health",
        "✓ Addresses the root cause naturally",
        "✓ Can be customized to your needs"
    ]
    
    return "\n".join(benefits)


def _generate_chemical_info(ingredients):
    """Generate information about active compounds"""
    compound_info = """
**Natural Active Compounds:**

• **Antioxidants:** Fight free radicals and prevent aging
• **Vitamins (A, C, E):** Promote healing and collagen production
• **Essential Fatty Acids:** Nourish and repair skin barrier
• **Natural Acids (Lactic, Citric):** Gentle exfoliation and brightening
• **Enzymes:** Break down dead skin cells and impurities
• **Anti-inflammatory Compounds:** Reduce redness and irritation
• **Antimicrobial Agents:** Fight bacteria and prevent infection

These compounds work synergistically to address your concern naturally and effectively.
"""
    return compound_info


def _generate_precautions(skin_type, allergies):
    """Generate safety precautions"""
    precautions = f"""
⚠️ **Important Safety Information:**

• Always perform a patch test 24 hours before full application
• Avoid contact with eyes - rinse immediately if contact occurs
• Discontinue use if you experience irritation, redness, or allergic reaction
• Not recommended for open wounds or broken skin
• Your skin type ({skin_type}) - adjust usage frequency accordingly
• Known allergies: {allergies} - avoid any ingredients you're allergic to
• Store in refrigerator and use within 3 days
• For external use only
• Consult a dermatologist for severe or persistent conditions
• Sun sensitivity may increase - use SPF protection
"""
    return precautions


# Alternative: If you want to use actual AI API in the future
def generate_ai_remedy_with_api(problem_description, available_ingredients, user):
    """
    This function can be used when you integrate an actual AI API like OpenAI
    For now, it's a placeholder that calls the template-based function
    """
    # TODO: Integrate with OpenAI GPT or other AI service
    # Example:
    # import openai
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[...]
    # )
    
    return generate_ai_remedy(problem_description, available_ingredients, user)
