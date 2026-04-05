"""
Script to populate the database with sample remedy data
Run this with: python manage.py shell < populate_data.py
"""

from remedies.models import Category, Problem, Remedy
from django.utils.text import slugify

print("Starting data population...")

# Create Categories
categories_data = [
    {
        'name': 'Skincare',
        'description': 'Natural remedies for healthy, glowing skin',
        'icon': 'fa-spa'
    },
    {
        'name': 'Hair Care',
        'description': 'Home remedies for beautiful, healthy hair',
        'icon': 'fa-cut'
    },
    {
        'name': 'Body Care',
        'description': 'Natural solutions for overall body wellness',
        'icon': 'fa-heart'
    },
    {
        'name': 'General Health and Wellness',
        'description': 'Home Remedies for minor health issues',
        'icon': 'fa-mortar-pestle'
    },
    {
        'name': 'Mental Health & Stress Relief',
        'description': 'Focuses on natural remedies and techniques to manage stress, anxiety, and improve mental well-being',
        'icon': 'fa-brain'
    },
    {
        'name': 'Women\'s Health',
        'description': 'Covers common health concerns related to women, including hormonal balance, menstrual health, and overall wellness',
        'icon': 'fa-venus'
    },
]

categories = {}
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        slug=slugify(cat_data['name']),
        defaults={
            'name': cat_data['name'],
            'description': cat_data['description'],
            'icon': cat_data['icon']
        }
    )
    categories[cat_data['name']] = category
    print(f"{'Created' if created else 'Found'} category: {category.name}")

# Create Problems
problems_data = [
    # Skincare Problems
    {
        'category': 'Skincare',
        'name': 'Acne and Pimples',
        'description': 'Inflammation and breakouts on the skin',
        'severity': 'moderate'
    },
    {
        'category': 'Skincare',
        'name': 'Dry Skin',
        'description': 'Lack of moisture causing flaky, tight skin',
        'severity': 'mild'
    },
    {
        'category': 'Skincare',
        'name': 'Dark Circles',
        'description': 'Darkening of skin under the eyes',
        'severity': 'mild'
    },
    {
        'category': 'Skincare',
        'name': 'Oily Skin',
        'description': 'Excess sebum production',
        'severity': 'mild'
    },
    # Hair Care Problems
    {
        'category': 'Hair Care',
        'name': 'Hair Fall',
        'description': 'Excessive hair loss and thinning',
        'severity': 'moderate'
    },
    {
        'category': 'Hair Care',
        'name': 'Dandruff',
        'description': 'Flaky, itchy scalp',
        'severity': 'mild'
    },
    {
        'category': 'Hair Care',
        'name': 'Dry Hair',
        'description': 'Brittle, rough hair texture',
        'severity': 'mild'
    },
    # Body Care Problems
    {
        'category': 'Body Care',
        'name': 'Cracked Heels',
        'description': 'Dry, cracked skin on feet',
        'severity': 'mild'
    },
    {
        'category': 'Body Care',
        'name': 'Body Odor',
        'description': 'Unpleasant body smell',
        'severity': 'mild'
    },
    # Mental Health & Stress Relief Problems
    {
        'category': 'Mental Health & Stress Relief',
        'name': 'Stress and Anxiety',
        'description': 'Persistent worry, nervousness, and anxiety symptoms',
        'severity': 'moderate'
    },
    {
        'category': 'Mental Health & Stress Relief',
        'name': 'Insomnia and Sleep Issues',
        'description': 'Difficulty falling asleep, staying asleep, or poor sleep quality',
        'severity': 'moderate'
    },
    {
        'category': 'Mental Health & Stress Relief',
        'name': 'Headaches and Migraines',
        'description': 'Recurring headaches and migraine pain',
        'severity': 'moderate'
    },
    {
        'category': 'Mental Health & Stress Relief',
        'name': 'Depression and Mood Swings',
        'description': 'Persistent sadness, low mood, and emotional instability',
        'severity': 'severe'
    },
    {
        'category': 'Mental Health & Stress Relief',
        'name': 'Memory Loss and Brain Fog',
        'description': 'Difficulty concentrating, forgetfulness, and mental fatigue',
        'severity': 'mild'
    },
    {
        'category': 'Mental Health & Stress Relief',
        'name': 'Fatigue and Low Energy',
        'description': 'Constant tiredness and lack of energy throughout the day',
        'severity': 'moderate'
    },
    # Women's Health Problems
    {
        'category': 'Women\'s Health',
        'name': 'Menstrual Cramps',
        'description': 'Pain and discomfort during menstrual cycle',
        'severity': 'moderate'
    },
    {
        'category': 'Women\'s Health',
        'name': 'Hormonal Imbalance',
        'description': 'Irregular periods, mood swings, and hormonal fluctuations',
        'severity': 'moderate'
    },
    {
        'category': 'Women\'s Health',
        'name': 'Fertility Issues',
        'description': 'Difficulty conceiving or subfertility concerns',
        'severity': 'moderate'
    },
    {
        'category': 'Women\'s Health',
        'name': 'Menopausal Symptoms',
        'description': 'Hot flashes, night sweats, mood changes, and other menopausal signs',
        'severity': 'moderate'
    },
    {
        'category': 'Women\'s Health',
        'name': 'Breast Tenderness',
        'description': 'Painful or tender breast tissue before menstruation',
        'severity': 'mild'
    },
    {
        'category': 'Women\'s Health',
        'name': 'Polycystic Ovary Syndrome (PCOS)',
        'description': 'Hormonal disorder affecting reproductive health',
        'severity': 'moderate'
    },
]

problems = {}
for prob_data in problems_data:
    problem, created = Problem.objects.get_or_create(
        category=categories[prob_data['category']],
        slug=slugify(prob_data['name']),
        defaults={
            'name': prob_data['name'],
            'description': prob_data['description'],
            'severity': prob_data['severity']
        }
    )
    problems[prob_data['name']] = problem
    print(f"{'Created' if created else 'Found'} problem: {problem.name}")

# Create Remedies
remedies_data = [
    # Acne Remedies
    {
        'problem': 'Acne and Pimples',
        'title': 'Honey and Cinnamon Face Mask',
        'description': 'A powerful antibacterial mask that fights acne-causing bacteria and reduces inflammation.',
        'ingredients': '''2 tablespoons organic honey
1 teaspoon cinnamon powder
1 teaspoon lemon juice (optional)''',
        'instructions': '''Mix honey and cinnamon powder in a clean bowl
Add lemon juice if using
Blend until you get a smooth paste
Apply to clean, dry face
Leave on for 15-20 minutes
Rinse with lukewarm water
Pat dry and moisturize''',
        'usage': 'Apply 2-3 times per week. Best used in the evening. Can be used as spot treatment or all-over face mask.',
        'benefits': '''Reduces acne and inflammation
Antibacterial properties fight acne-causing bacteria
Soothes irritated skin
Prevents future breakouts
Natural and gentle on skin''',
        'chemicals': 'Honey contains hydrogen peroxide (antibacterial), Cinnamon contains cinnamaldehyde (anti-inflammatory)',
        'reactions': 'Hydrogen peroxide kills acne bacteria. Cinnamaldehyde reduces swelling and redness.',
        'importance': 'This combination has been used for centuries due to its powerful antimicrobial properties.',
        'precautions': '''Patch test before use
Avoid if allergic to honey or cinnamon
May cause tingling sensation (normal)
Avoid contact with eyes
Not suitable for open wounds''',
        'preparation_time': '5 minutes',
        'effectiveness_rating': 8
    },
    # Dry Skin Remedies
    {
        'problem': 'Dry Skin',
        'title': 'Avocado and Honey Moisturizing Mask',
        'description': 'Deep hydration mask that nourishes and restores moisture to dry skin.',
        'ingredients': '''1/2 ripe avocado
1 tablespoon honey
1 tablespoon plain yogurt
1 teaspoon olive oil''',
        'instructions': '''Mash avocado in a bowl until smooth
Add honey, yogurt, and olive oil
Mix well until creamy
Apply evenly to clean face and neck
Leave on for 20-30 minutes
Rinse with lukewarm water
Gently pat dry''',
        'usage': 'Use 2-3 times per week. Can be applied to face, neck, and other dry areas. Best used after shower.',
        'benefits': '''Deep moisturization
Provides essential fatty acids
Soothes dry, flaky skin
Restores skin barrier
Natural glow
Anti-aging properties''',
        'chemicals': 'Avocado oils (omega-3, omega-6), Vitamin E, Lactic acid from yogurt',
        'reactions': 'Fatty acids penetrate skin barrier, lactic acid gently exfoliates, honey humectant properties retain moisture.',
        'importance': 'Avocado is rich in healthy fats that deeply nourish dry skin naturally.',
        'precautions': '''Patch test recommended
Use ripe avocados only
Store leftovers in refrigerator (use within 2 days)
Avoid if allergic to any ingredients
Normal skin may find it too heavy''',
        'preparation_time': '10 minutes',
        'effectiveness_rating': 9
    },
    # Hair Fall Remedy
    {
        'problem': 'Hair Fall',
        'title': 'Onion Juice Hair Treatment',
        'description': 'Stimulates hair growth and strengthens hair follicles naturally.',
        'ingredients': '''2-3 medium onions
1 tablespoon coconut oil
1 teaspoon honey (optional)
Few drops of essential oil (to mask smell)''',
        'instructions': '''Peel and chop onions
Blend or juice to extract liquid
Strain to remove pulp
Mix with coconut oil and honey
Apply to scalp using cotton ball
Massage gently for 5 minutes
Cover with shower cap
Leave for 30 minutes to 1 hour
Wash with mild shampoo (may need 2 washes)''',
        'usage': 'Apply 2-3 times per week. Best results seen after 2-3 months of consistent use. Use on scalp only, avoid lengths.',
        'benefits': '''Stimulates hair growth
Strengthens hair follicles
Improves blood circulation to scalp
Rich in sulfur for hair protein
Reduces hair fall
Adds shine and thickness''',
        'chemicals': 'Sulfur compounds, Quercetin (antioxidant), Vitamin C',
        'reactions': 'Sulfur promotes collagen production and keratin synthesis. Quercetin improves blood flow to hair follicles.',
        'importance': 'Onion juice is scientifically proven to promote hair regrowth in studies.',
        'precautions': '''Strong smell (add essential oils)
May cause scalp irritation in some people
Patch test on small scalp area first
Avoid contact with eyes
Rinse thoroughly
Not recommended for sensitive scalps''',
        'preparation_time': '15 minutes',
        'effectiveness_rating': 9
    },
    # Dandruff Remedy
    {
        'problem': 'Dandruff',
        'title': 'Coconut Oil and Lemon Scalp Treatment',
        'description': 'Moisturizes scalp while controlling dandruff-causing fungus.',
        'ingredients': '''3 tablespoons coconut oil
2 tablespoons fresh lemon juice
1 teaspoon tea tree oil (optional)''',
        'instructions': '''Warm coconut oil (not hot)
Add lemon juice and tea tree oil
Mix well
Part hair in sections
Apply to scalp
Massage for 5-10 minutes
Leave on for 30 minutes
Wash with anti-dandruff shampoo''',
        'usage': 'Use 2-3 times per week. Apply to scalp only. Best done before shower.',
        'benefits': '''Eliminates dandruff
Moisturizes dry scalp
Antifungal properties
Reduces itching
Promotes healthy scalp
Conditions hair''',
        'chemicals': 'Lauric acid (coconut oil), Citric acid (lemon), Tea tree oil compounds',
        'reactions': 'Lauric acid has antifungal properties. Citric acid balances pH. Tea tree oil kills dandruff-causing fungus.',
        'importance': 'Coconut oil and lemon combination addresses both dry scalp and fungal causes of dandruff.',
        'precautions': '''Lemon may lighten hair color
Patch test before use
Avoid if you have colored hair
May sting if scalp has scratches
Rinse thoroughly
Sun sensitivity - use in evening''',
        'preparation_time': '5 minutes',
        'effectiveness_rating': 8
    },
    # Dark Circles Remedy
    {
        'problem': 'Dark Circles',
        'title': 'Cucumber and Potato Eye Treatment',
        'description': 'Cooling treatment that reduces puffiness and lightens dark circles.',
        'ingredients': '''1/2 cucumber (chilled)
1 small potato
1 teaspoon rose water
Cotton pads''',
        'instructions': '''Grate cucumber and potato
Extract juice using strainer
Mix juices with rose water
Soak cotton pads in mixture
Place on closed eyes
Relax for 15-20 minutes
Rinse with cool water
Pat dry gently''',
        'usage': 'Daily application for best results. Morning and/or evening. Use chilled for extra cooling effect.',
        'benefits': '''Reduces dark circles
Lightens pigmentation
Reduces puffiness
Cools and soothes
Hydrates delicate eye area
Natural and safe''',
        'chemicals': 'Vitamin C (cucumber), Catecholase enzyme (potato), Natural bleaching agents',
        'reactions': 'Vitamin C brightens skin. Catecholase enzyme lightens pigmentation. Cucumber cools and reduces inflammation.',
        'importance': 'Both cucumber and potato are gentle yet effective for the sensitive eye area.',
        'precautions': '''Keep eyes closed during application
Use fresh ingredients
Store excess in refrigerator (1-2 days)
Avoid if skin is broken
Discontinue if irritation occurs
For external use only''',
        'preparation_time': '10 minutes',
        'effectiveness_rating': 7
    },
]

for remedy_data in remedies_data:
    remedy, created = Remedy.objects.get_or_create(
        problem=problems[remedy_data['problem']],
        title=remedy_data['title'],
        defaults={
            'description': remedy_data['description'],
            'ingredients': remedy_data['ingredients'],
            'instructions': remedy_data['instructions'],
            'usage': remedy_data['usage'],
            'benefits': remedy_data['benefits'],
            'chemicals': remedy_data['chemicals'],
            'reactions': remedy_data['reactions'],
            'importance': remedy_data['importance'],
            'precautions': remedy_data['precautions'],
            'preparation_time': remedy_data['preparation_time'],
            'effectiveness_rating': remedy_data['effectiveness_rating']
        }
    )
    print(f"{'Created' if created else 'Found'} remedy: {remedy.title}")

print("\nData population completed successfully!")
print(f"Categories: {Category.objects.count()}")
print(f"Problems: {Problem.objects.count()}")
print(f"Remedies: {Remedy.objects.count()}")
