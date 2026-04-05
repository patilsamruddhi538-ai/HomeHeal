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
        'icon': 'fa-heart-pulse'
    },
    {
        'name': 'Mental Health & Stress Relief',
        'description': 'Focuses on natural remedies and techniques to manage stress, anxiety, and improve mental well-being',
        'icon': 'fa-leaf'
    },
    {
        'name': 'Women\'s Health',
        'description': 'Covers common health concerns related to women, including hormonal balance, menstrual health, and overall wellness',
        'icon': 'fa-flower'
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
    # Mental Health & Stress Relief Remedies
    {
        'problem': 'Stress and Anxiety',
        'title': 'Chamomile and Lavender Tea',
        'description': 'Calming herbal tea that reduces anxiety and promotes relaxation.',
        'ingredients': '''2 tablespoons dried chamomile flowers
1 tablespoon dried lavender flowers
1 teaspoon honey
1 cup hot water''',
        'instructions': '''Heat water to boiling
Add chamomile and lavender to a tea cup
Pour hot water over herbs
Steep for 5-7 minutes
Strain the herbs
Add honey to taste
Sip slowly and inhale the steam''',
        'usage': 'Drink 1-2 cups daily, preferably in the morning or evening. Can be taken during stressful situations for immediate relief.',
        'benefits': '''Reduces anxiety and stress
Promotes calmness
Improves sleep quality
Relaxes muscles
Soothes nervous system
Natural and gentle''',
        'chemicals': 'Apigenin (chamomile), Linalool (lavender), Coumarin compounds',
        'reactions': 'Apigenin binds to brain receptors promoting relaxation. Linalool has anxiolytic properties. Together they enhance calming effects.',
        'importance': 'Both herbs have been used for centuries in traditional medicine for anxiety relief.',
        'precautions': '''Avoid if pregnant or nursing
May cause drowsiness
Discontinue if allergic reactions occur
Not suitable as replacement for medical treatment
Consult doctor if taking sedative medications''',
        'preparation_time': '10 minutes',
        'effectiveness_rating': 8
    },
    {
        'problem': 'Insomnia and Sleep Issues',
        'title': 'Warm Turmeric and Almond Milk',
        'description': 'Soothing bedtime drink that promotes deep, restful sleep.',
        'ingredients': '''1 cup unsweetened almond milk
1/2 teaspoon turmeric powder
1/4 teaspoon cinnamon powder
1 pinch black pepper
1 teaspoon honey (optional)
1 pinch nutmeg''',
        'instructions': '''Warm almond milk in a pan (do not boil)
Add turmeric, cinnamon, and black pepper
Stir well for 2 minutes
Pour into a cup
Add honey if desired
Sprinkle nutmeg on top
Drink warm before bedtime''',
        'usage': 'Drink 30 minutes before sleep. Consume daily for best results. Can be prepared fresh or in batches.',
        'benefits': '''Promotes deep sleep
Relaxes muscles
Reduces inflammation
Calms mind
Balances sleep-wake cycle
Improves sleep quality''',
        'chemicals': 'Curcumin (turmeric), Cinnamaldehyde (cinnamon), Myristicin (nutmeg)',
        'reactions': 'Curcumin reduces inflammation affecting sleep. Cinnamon regulates blood sugar for stable energy. Nutmeg contains sedative compounds.',
        'importance': 'Turmeric has proven sleep-enhancing and anti-inflammatory properties studied in traditional Ayurvedic medicine.',
        'precautions': '''Avoid if allergic to turmeric
May stain clothes
Not recommended during pregnancy in large quantities
Wait 2 hours after meals for better absorption
Consult doctor if taking blood thinners''',
        'preparation_time': '5 minutes',
        'effectiveness_rating': 8
    },
    {
        'problem': 'Headaches and Migraines',
        'title': 'Ginger and Peppermint Tea',
        'description': 'Powerful herbal remedy that relieves headaches and migraines naturally.',
        'ingredients': '''1 inch fresh ginger root (sliced)
1 tablespoon dried peppermint leaves
1 cup water
1 teaspoon honey
Few drops lemon juice''',
        'instructions': '''Boil water and add sliced ginger
Simmer for 5 minutes
Remove from heat and add peppermint
Steep for 3-5 minutes
Strain into a cup
Add honey and lemon juice
Drink while warm''',
        'usage': 'Drink at the first sign of headache. Can consume 2-3 times daily during migraine attacks. Drink slowly.',
        'benefits': '''Relieves headache pain
Reduces migraine frequency
Improves blood circulation
Anti-inflammatory
Reduces nausea
Soothes nervous tension''',
        'chemicals': 'Gingerol and shogaol (ginger), Menthol (peppermint), Citric acid (lemon)',
        'reactions': 'Gingerol blocks inflammatory substances. Menthol cools and relaxes muscles. Combined effect enhances pain relief.',
        'importance': 'Ginger has been scientifically proven as effective as some migraine medications without side effects.',
        'precautions': '''May cause heartburn in some people
Avoid if taking blood thinners
High doses may cause nausea
Consult doctor before use if pregnant
May interact with migraine medications''',
        'preparation_time': '10 minutes',
        'effectiveness_rating': 9
    },
    {
        'problem': 'Depression and Mood Swings',
        'title': 'Ashwagandha and Brahmi Herbal Supplement',
        'description': 'Ancient Ayurvedic adaptogens that balance mood and improve emotional resilience.',
        'ingredients': '''1 teaspoon Ashwagandha powder
1 teaspoon Brahmi powder
1 cup warm milk or water
1 teaspoon honey
1 pinch black pepper''',
        'instructions': '''Mix Ashwagandha and Brahmi powders in a bowl
Add warm milk or water gradually
Stir until smooth paste forms
Add honey and black pepper
Mix well
Drink the mixture
Consume on empty stomach for best absorption''',
        'usage': 'Take once daily in morning on empty stomach. Consistent use for 30-45 days shows best results. Can continue long-term.',
        'benefits': '''Improves mood naturally
Reduces depression symptoms
Stabilizes emotions
Enhances emotional resilience
Promotes mental clarity
Reduces emotional stress''',
        'chemicals': 'Withanolides (Ashwagandha), Alkaloids (Brahmi), Saponins',
        'reactions': 'Withanolides modulate stress hormones. Brahmi alkaloids enhance neurotransmitter function. Together they stabilize mood naturally.',
        'importance': 'Ashwagandha and Brahmi are traditional Ayurvedic remedies scientifically validated for mood support.',
        'precautions': '''Not for pregnant or nursing women
May cause drowsiness
Avoid with sedatives
Take adequate gap from other medications
Consult healthcare provider if on antidepressants
May take 4-6 weeks to show full effects''',
        'preparation_time': '5 minutes',
        'effectiveness_rating': 8
    },
    {
        'problem': 'Memory Loss and Brain Fog',
        'title': 'Brahmi and Rosemary Brain Tonic',
        'description': 'Cognitive enhancing herbal remedy that clears brain fog and improves memory.',
        'ingredients': '''2 teaspoons Brahmi powder
1 teaspoon dried rosemary (or fresh)
1 cup water
1/2 teaspoon ghee (clarified butter)
1 teaspoon honey
Pinch of salt''',
        'instructions': '''Boil water and add rosemary
Simmer for 3-4 minutes
Remove from heat and cool slightly
Add Brahmi powder and stir well
Add ghee and honey
Mix thoroughly
Drink warm on empty stomach''',
        'usage': 'Consume once daily in morning on empty stomach. Best taken consistently for 60 days to see marked improvement.',
        'benefits': '''Improves memory and focus
Clears mental fog
Enhances concentration
Supports brain health
Promotes mental clarity
Reduces forgetfulness''',
        'chemicals': 'Bacosides (Brahmi), Carnosic acid (Rosemary), Volatile oils',
        'reactions': 'Bacosides enhance synaptic transmission. Carnosic acid protects neurons. Ghee aids absorption and supports brain function.',
        'importance': 'Brahmi is traditionally used in Ayurveda as a Medhya (intelligence-promoting) herb with proven clinical efficacy.',
        'precautions': '''Not recommended during pregnancy
May cause drowsiness initially
Avoid with blood thinners
Can take 4-8 weeks for optimal results
Discontinue if allergic reactions occur''',
        'preparation_time': '10 minutes',
        'effectiveness_rating': 8
    },
    {
        'problem': 'Fatigue and Low Energy',
        'title': 'Ginseng and Date Energy Tonic',
        'description': 'Energizing herbal remedy that boosts stamina and fights fatigue naturally.',
        'ingredients': '''1 teaspoon Ginseng powder (or 1 inch dried ginseng root)
3-4 pitted dates
1 cup water
1/2 teaspoon honey
Few drops lemon juice
1 pinch cardamom powder''',
        'instructions': '''Boil water and add ginseng
Simmer for 5 minutes
Add dates and simmer for 2 minutes
Remove from heat
Add honey, lemon juice, and cardamom
Blend until smooth or drink as is
Consume while warm''',
        'usage': 'Drink once daily in morning for sustained energy. Can take on empty stomach or with light breakfast.',
        'benefits': '''Boosts energy and stamina
Reduces fatigue
Improves physical endurance
Enhances mental alertness
Supports immune function
Promotes overall vitality''',
        'chemicals': 'Ginsenosides (Ginseng), Natural sugars (dates), Vitamins and minerals',
        'reactions': 'Ginsenosides increase ATP production for energy. Dates provide natural sustained energy. Combined they fight fatigue effectively.',
        'importance': 'Ginseng is scientifically proven to increase energy levels and reduce fatigue in multiple clinical studies.',
        'precautions': '''May cause insomnia if taken late
Not suitable for high blood pressure
Avoid with stimulants
May increase heart rate in some people
Consult doctor if taking medications
Not for pregnant women''',
        'preparation_time': '10 minutes',
        'effectiveness_rating': 9
    },
    # Women's Health Remedies
    {
        'problem': 'Menstrual Cramps',
        'title': 'Ginger and Turmeric Cramp Relief Tea',
        'description': 'Anti-inflammatory herbal tea that provides natural relief from menstrual cramps.',
        'ingredients': '''1 inch fresh ginger root (sliced)
1/2 teaspoon turmeric powder
1 cup water
1 teaspoon honey
Pinch of cinnamon
Few drops lemon juice''',
        'instructions': '''Boil water and add ginger slices
Simmer for 5 minutes
Add turmeric powder and cinnamon
Stir well and simmer for 2 minutes
Remove from heat
Add honey and lemon juice
Sip slowly''',
        'usage': 'Drink 2-3 times daily during menstrual cycle, especially when cramps occur. Start 1-2 days before period begins.',
        'benefits': '''Reduces cramp pain
Relieves muscle tension
Anti-inflammatory
Relaxes uterine muscles
Improves blood flow
Eases discomfort''',
        'chemicals': 'Gingerol, Curcumin (turmeric), Cinnamaldehyde',
        'reactions': 'Gingerol and Curcumin reduce prostaglandins causing cramps. Cinnamon relaxes muscles and improves circulation.',
        'importance': 'Ginger has been clinically proven to be as effective as ibuprofen for menstrual pain relief.',
        'precautions': '''Avoid large amounts if on blood thinners
May slightly increase period flow
Discontinue if excessive bleeding occurs
Not suitable in early pregnancy
Consult doctor if severe cramps persist''',
        'preparation_time': '10 minutes',
        'effectiveness_rating': 9
    },
    {
        'problem': 'Hormonal Imbalance',
        'title': 'Flaxseed and Fenugreek Hormone Balance Drink',
        'description': 'Natural remedy that helps balance hormones and regulate menstrual cycles.',
        'ingredients': '''1 tablespoon ground flaxseed
1/2 teaspoon fenugreek powder
1 cup warm water or milk
1 teaspoon honey
1 pinch nutmeg''',
        'instructions': '''Mix flaxseed and fenugreek powder in a bowl
Add warm water or milk slowly
Stir well to avoid lumps
Add honey and nutmeg
Mix thoroughly
Drink the mixture without straining
Consume immediately after preparation''',
        'usage': 'Take once daily in morning on empty stomach. Consistent use for 3 months shows best hormonal balance results.',
        'benefits': '''Balances hormones naturally
Regulates menstrual cycle
Reduces PMS symptoms
Improves fertility
Supports reproductive health
Stabilizes mood fluctuations''',
        'chemicals': 'Lignans (flaxseed), Diosgenin (fenugreek), Phytoestrogens',
        'reactions': 'Lignans convert to phytoestrogens supporting hormone balance. Diosgenin mimics female hormones for cycle regulation.',
        'importance': 'Flaxseed lignans have been researched for natural hormone balancing without synthetic interventions.',
        'precautions': '''May cause bloating initially
Increase water intake
Not recommended during pregnancy
May interact with hormone medications
Discontinue if allergic reactions occur
Consult doctor if on birth control''',
        'preparation_time': '5 minutes',
        'effectiveness_rating': 8
    },
    {
        'problem': 'Fertility Issues',
        'title': 'Maca Root and Red Clover Fertility Enhancer',
        'description': 'Nutrient-rich herbal supplement designed to support fertility and reproductive health.',
        'ingredients': '''1 teaspoon Maca root powder
1/2 teaspoon dried red clover flowers
1 cup warm milk or water
1/2 teaspoon honey
Pinch of saffron (optional)''',
        'instructions': '''Warm milk or water slightly
Add Maca powder and red clover
Stir until well combined
Add saffron and honey
Mix thoroughly
Let steep for 2 minutes
Drink warm or room temperature''',
        'usage': 'Consume once daily in morning. For best fertility results, continue for 2-3 months. Should be part of holistic fertility plan.',
        'benefits': '''Enhances fertility
Improves reproductive health
Increases vitality
Balances hormones
Improves egg quality
Increases sexual function''',
        'chemicals': 'Macamides (Maca), Isoflavones (red clover), Phenolic compounds',
        'reactions': 'Macamides improve sexual function and fertility. Isoflavones support hormone balance crucial for conception.',
        'importance': 'Maca has shown promising results in clinical studies for improving fertility outcomes in both men and women.',
        'precautions': '''Not for pregnant women
May increase sexual appetite
Avoid if thyroid issues (use small amounts)
Not a replacement for medical treatment
Consult fertility specialist
May take 2-3 months for effects''',
        'preparation_time': '5 minutes',
        'effectiveness_rating': 8
    },
    {
        'problem': 'Menopausal Symptoms',
        'title': 'Black Cohosh and Sage Herbal Remedy',
        'description': 'Traditional herbal formula that eases hot flashes and menopausal discomfort.',
        'ingredients': '''1/2 teaspoon dried Black Cohosh root
1 teaspoon dried sage leaves
1 cup water
1 teaspoon honey
Few drops vanilla extract (optional)''',
        'instructions': '''Boil water and add Black Cohosh
Simmer for 5 minutes
Remove from heat and add sage leaves
Steep for 5 minutes
Strain the mixture
Add honey and vanilla
Drink warm or cool as preferred''',
        'usage': 'Drink 1-2 cups daily. Continue for several weeks to see reduction in hot flashes and night sweats.',
        'benefits': '''Reduces hot flashes
Alleviates night sweats
Improves mood during menopause
Promotes better sleep
Reduces anxiety
Supports hormonal transition''',
        'chemicals': 'Triterpenes (Black Cohosh), Salvia compounds (sage), Flavonoids',
        'reactions': 'Triterpenes bind to estrogen receptors easing hot flashes. Sage reduces perspiration and improves mood stability.',
        'importance': 'Black Cohosh is one of the most researched herbal remedies for menopausal symptom relief globally.',
        'precautions': '''Not for pregnant women
May take 2-4 weeks to see results
Avoid if liver disease
Monitor for side effects
Consult doctor if on hormone therapy
Not suitable for estrogen-sensitive conditions''',
        'preparation_time': '10 minutes',
        'effectiveness_rating': 8
    },
    {
        'problem': 'Breast Tenderness',
        'title': 'Vitamin E and Evening Primrose Oil Treatment',
        'description': 'Natural oil treatment that reduces breast tenderness and sensitivity.',
        'ingredients': '''2 capsules Vitamin E oil (or 1 teaspoon oil)
1 teaspoon Evening Primrose Oil
1/4 teaspoon coconut oil (carrier oil)
Optional: 2 drops lavender essential oil''',
        'instructions': '''Combine Vitamin E and Evening Primrose oils
Add coconut oil as carrier
Add lavender oil if desired
Mix gently in a small bowl
Apply directly to breast area
Massage gently in circular motions
Use daily before bed
Leave on overnight or for 2-3 hours''',
        'usage': 'Apply daily, preferably at night. Continue consistently for 4-6 weeks for visible relief. Most effective in luteal phase.',
        'benefits': '''Reduces breast tenderness
Alleviates sensitivity
Hormonal balance support
Anti-inflammatory
Improves breast tissue health
Natural pain relief''',
        'chemicals': 'Vitamin E (tocopherol), Gamma-linolenic acid (GLA from evening primrose)',
        'reactions': 'Vitamin E reduces inflammation. GLA hormone precursors balance hormonal fluctuations causing tenderness.',
        'importance': 'Evening Primrose Oil GLA content is scientifically documented for cyclic breast tenderness relief.',
        'precautions': '''Avoid contact with eyes
Do patch test first
May cause allergic reaction
Not for pregnant women
May take 4-6 weeks for results
Discontinue if skin irritation occurs''',
        'preparation_time': '5 minutes',
        'effectiveness_rating': 8
    },
    {
        'problem': 'Polycystic Ovary Syndrome (PCOS)',
        'title': 'Spearmint Tea and Inositol Supplement',
        'description': 'Natural PCOS management remedy combining hormone regulation and insulin balance.',
        'ingredients': '''1 tablespoon dried spearmint leaves
1 cup water
1/2 teaspoon inositol powder
1 teaspoon honey
Few drops lemon juice
1 pinch cinnamon''',
        'instructions': '''Boil water and add spearmint leaves
Simmer for 10 minutes
Remove from heat and strain
Add inositol powder and stir well
Add honey, lemon juice, and cinnamon
Mix thoroughly
Drink warm''',
        'usage': 'Drink 2 times daily for consistent results. Continue for 3-6 months to see significant hormonal improvements in PCOS symptoms.',
        'benefits': '''Reduces androgen levels
Improves insulin sensitivity
Regulates menstrual cycle
Reduces excess hair growth
Supports fertility
Helps manage weight''',
        'chemicals': 'Flavones (spearmint), Myo-inositol and D-chiro-inositol',
        'reactions': 'Spearmint reduces excess androgens. Inositol improves insulin signaling and hormonal balance crucial for PCOS management.',
        'importance': 'Spearmint tea and inositol supplementation are recommended interventions in clinical PCOS management protocols.',
        'precautions': '''Long-term commitment required
May interact with diabetes medications
Not a replacement for medical treatment
Requires dietary and lifestyle changes
Consult endocrinologist regularly
Monitor blood sugar levels''',
        'preparation_time': '10 minutes',
        'effectiveness_rating': 9
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
