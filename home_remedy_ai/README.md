# HomeHeal - Natural Home Remedies Platform 🌿

A comprehensive Django web application for discovering, sharing, and getting AI-powered recommendations for natural home remedies.

## Features

### 🔐 User Management
- **Sign Up & Login**: Secure user authentication system
- **User Profiles**: Personalized profiles with skin type, hair type, age, and allergy information
- **Profile Pictures**: Upload and manage profile pictures

### 🌿 Remedy System
- **Categories**: Browse remedies by category (Skincare, Hair Care, Body Care)
- **Problems**: Explore specific problems within each category
- **Detailed Remedies**: Complete information including:
  - Ingredients list
  - Step-by-step instructions
  - Usage guidelines
  - Benefits
  - Active chemical compounds
  - How chemicals react
  - Importance and science behind the remedy
  - Precautions and warnings
  - Preparation time
  - Effectiveness rating

### ❤️ User Features
- **Favorites**: Save your favorite remedies for quick access
- **Search**: Search across all remedies, problems, and ingredients
- **Responsive Design**: Beautiful, modern UI that works on all devices

### 🤖 AI-Powered Consultation
- **Custom Recommendations**: Get personalized remedy suggestions based on:
  - Your specific problem description
  - Available ingredients at home
  - Your profile information (skin type, allergies)
- **Consultation History**: View and revisit your past AI consultations

## Technology Stack

- **Backend**: Django 6.0
- **Database**: SQLite (can be upgraded to PostgreSQL/MySQL)
- **Frontend**: 
  - Bootstrap 5 for responsive design
  - Font Awesome for icons
  - Google Fonts (Poppins)
- **AI Engine**: Live OpenAI integration with automatic smart fallback

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Activate Virtual Environment

```bash
cd "E:\PCCOE\INFORMATION TECHNOLOGY\ROOMATE'S PROJECT\HomeHeal"
.\venv\Scripts\activate
```

### Step 2: Navigate to Project Directory

```bash
cd home_remedy_ai
```

### Step 3: Install Dependencies

```bash
pip install django pillow
```

### Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 6: Populate Sample Data

```bash
python manage.py shell < populate_data.py
```

This will create:
- 3 Categories (Skincare, Hair Care, Body Care)
- 9 Problems
- 5 Detailed Remedies

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

### Optional: Enable Real OpenAI Responses

1. Create a local env file in the project root:

```bash
copy .env.example .env
```

2. Open `.env` and set your real key:

```env
OPENAI_API_KEY=your_real_openai_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_TIMEOUT=25
```

3. Restart Django server after updating `.env`.

If key is missing or invalid, consultations still work using smart local fallback mode.

### Step 8: Access the Application

Open your browser and navigate to:
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Project Structure

```
home_remedy_ai/
├── accounts/                 # User authentication & profiles
│   ├── models.py            # Profile model
│   ├── views.py             # Login, signup, profile views
│   ├── forms.py             # User forms
│   └── admin.py             # Admin configuration
├── remedies/                 # Main remedy system
│   ├── models.py            # Category, Problem, Remedy models
│   ├── views.py             # All remedy views
│   ├── admin.py             # Admin configuration
│   └── ...
├── ai_engine/                # AI recommendation engine
│   ├── services.py          # AI logic and algorithms
│   └── utils.py             # Helper functions
├── templates/                # HTML templates
│   ├── base.html            # Base template with navigation
│   ├── accounts/            # Authentication templates
│   └── remedies/            # Remedy-related templates
├── static/                   # Static files (CSS, JS, images)
├── media/                    # User uploads (profile pictures)
├── home_remedy_ai/          # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── ...
├── manage.py                 # Django management script
└── populate_data.py          # Sample data population script
```

## Usage Guide

### For Regular Users

1. **Sign Up**: Create an account with username, email, and password
2. **Update Profile**: Add your age, skin type, hair type, and known allergies
3. **Browse Categories**: Explore Skincare, Hair Care, or Body Care
4. **Select Problem**: Choose a specific problem you're facing
5. **View Remedies**: Browse available natural remedies
6. **Save Favorites**: Click the heart icon to save remedies
7. **AI Consultation**: Get custom recommendations based on available ingredients

### For Administrators

1. **Login to Admin**: http://127.0.0.1:8000/admin/
2. **Add Content**:
   - Create new categories
   - Add problems to categories
   - Create detailed remedies
   - Moderate user consultations
3. **Manage Users**: View and manage user profiles

## Adding New Remedies

### Via Admin Panel

1. Login to admin panel
2. Navigate to "Remedies" → "Add Remedy"
3. Fill in all fields:
   - Select problem
   - Enter title and description
   - List ingredients (one per line)
   - Provide step-by-step instructions
   - Add usage guidelines
   - List benefits
   - Include chemical information
   - Add precautions
   - Set preparation time and effectiveness rating
4. Save

### Programmatically

```python
from remedies.models import Category, Problem, Remedy

# Get or create problem
problem = Problem.objects.get(name="Your Problem")

# Create remedy
Remedy.objects.create(
    problem=problem,
    title="Remedy Title",
    description="Brief description",
    ingredients="Ingredient 1\nIngredient 2",
    instructions="Step 1\nStep 2",
    usage="How to use",
    benefits="Benefit 1\nBenefit 2",
    precautions="Safety information",
    effectiveness_rating=8
)
```

## AI Consultation System

The AI consultation feature first attempts a real OpenAI call and then falls back to local smart generation if needed:

1. Analyzes the user's problem description
2. Matches available ingredients with known remedies
3. Considers user's profile (skin type, allergies)
4. Generates personalized recommendations with:
   - Ingredient measurements
   - Preparation instructions
   - Usage guidelines
   - Benefits and active compounds
   - Personalized precautions

Fallback mode ensures users can still submit and receive guidance even during missing key, quota limits, or network issues.

## Customization

### Changing Colors

Edit `templates/base.html` CSS variables:

```css
:root {
    --primary-color: #2ecc71;      /* Main green */
    --secondary-color: #27ae60;    /* Dark green */
    --accent-color: #3498db;       /* Blue accent */
    --gradient-start: #56ab2f;     /* Gradient start */
    --gradient-end: #a8e063;       /* Gradient end */
}
```

### Adding New Categories

1. Admin panel or Django shell:

```python
from remedies.models import Category
from django.utils.text import slugify

Category.objects.create(
    name="Oral Care",
    slug="oral-care",
    description="Natural remedies for dental health",
    icon="fa-tooth"
)
```

## Database Schema

### Core Models

- **Category**: Main remedy categories
- **Problem**: Specific issues within categories
- **Remedy**: Detailed remedy information
- **Profile**: Extended user information
- **UserFavorite**: User's saved remedies
- **AIConsultation**: AI consultation history

## Security Notes

⚠️ **For Production Deployment**:

1. Change `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Set up HTTPS
6. Use PostgreSQL or MySQL instead of SQLite
7. Configure static files properly
8. Set up proper email backend
9. Implement rate limiting
10. Regular security updates

## Contributing

To add more remedies:

1. Research and verify the remedy
2. Include scientific backing if possible
3. Always include precautions
4. Test for allergic reactions
5. Cite sources when applicable

## Support & Troubleshooting

### Common Issues

**Issue**: Cannot login after signup
- **Solution**: Make sure you activated your virtual environment and migrations are applied

**Issue**: Images not loading
- **Solution**: Run `python manage.py collectstatic` and check MEDIA settings

**Issue**: AI consultation not working
- **Solution**: Check `.env` in project root has a valid `OPENAI_API_KEY`, then restart server

### Getting Help

- Check Django documentation: https://docs.djangoproject.com/
- Review code comments in files
- Check error logs in terminal

## Future Enhancements

- [ ] Mobile app version
- [ ] User reviews and ratings
- [ ] Video tutorials for remedies
- [ ] Community forum
- [ ] Ingredient marketplace integration
- [ ] Multi-language support
- [ ] Advanced AI with image recognition
- [ ] Remedy effectiveness tracking
- [ ] Social sharing features
- [ ] Email notifications

## License

This project is for educational purposes. Always consult healthcare professionals for serious health concerns.

## Disclaimer

⚠️ **Important Health Notice**:
- Home remedies are not substitutes for professional medical advice
- Always perform patch tests before applying anything to skin
- Consult a doctor for serious or persistent conditions
- Individual results may vary
- Discontinue use if irritation occurs

## Credits

- Built with Django Framework
- UI: Bootstrap 5 & Font Awesome
- Fonts: Google Fonts (Poppins)
- Icons: Font Awesome

---

**Developed for natural wellness and education** 🌿

For questions or contributions, please update the repository or contact the development team.
