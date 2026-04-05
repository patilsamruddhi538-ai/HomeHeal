from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Category, Problem, Remedy, UserFavorite, AIConsultation
from ai_engine.services import generate_ai_remedy, parse_ai_remedy_payload

def home(request):
    """Homepage with category showcase"""
    categories = Category.objects.all()
    popular_remedies = Remedy.objects.order_by('-effectiveness_rating')[:6]
    
    context = {
        'categories': categories,
        'popular_remedies': popular_remedies,
    }
    return render(request, 'remedies/home.html', context)

def categories_view(request):
    """Display all categories"""
    categories = Category.objects.annotate(problem_count=Count('problems'))
    return render(request, 'remedies/categories.html', {'categories': categories})

def category_detail(request, slug):
    """Show problems within a category"""
    category = get_object_or_404(Category, slug=slug)
    problems = category.problems.all()
    
    context = {
        'category': category,
        'problems': problems,
    }
    return render(request, 'remedies/category_detail.html', context)

def problem_detail(request, category_slug, problem_slug):
    """Show remedies for a specific problem"""
    category = get_object_or_404(Category, slug=category_slug)
    problem = get_object_or_404(Problem, category=category, slug=problem_slug)
    remedies = problem.remedies.all()
    
    context = {
        'category': category,
        'problem': problem,
        'remedies': remedies,
    }
    return render(request, 'remedies/problem_detail.html', context)

def remedy_detail(request, remedy_id):
    """Detailed view of a remedy"""
    remedy = get_object_or_404(Remedy, id=remedy_id)
    is_favorite = False
    
    if request.user.is_authenticated:
        is_favorite = UserFavorite.objects.filter(user=request.user, remedy=remedy).exists()
    
    # Parse ingredients and instructions as lists
    ingredients_list = [ing.strip() for ing in remedy.ingredients.split('\n') if ing.strip()]
    instructions_list = [inst.strip() for inst in remedy.instructions.split('\n') if inst.strip()]
    benefits_list = [ben.strip() for ben in remedy.benefits.split('\n') if ben.strip()]
    
    context = {
        'remedy': remedy,
        'is_favorite': is_favorite,
        'ingredients_list': ingredients_list,
        'instructions_list': instructions_list,
        'benefits_list': benefits_list,
    }
    return render(request, 'remedies/remedy_detail.html', context)

@login_required
def toggle_favorite(request, remedy_id):
    """Add or remove remedy from favorites"""
    remedy = get_object_or_404(Remedy, id=remedy_id)
    favorite, created = UserFavorite.objects.get_or_create(user=request.user, remedy=remedy)
    
    if not created:
        favorite.delete()
        messages.info(request, 'Removed from favorites.')
    else:
        messages.success(request, 'Added to favorites!')
    
    return redirect('remedy_detail', remedy_id=remedy_id)

@login_required
def favorites_view(request):
    """User's favorite remedies"""
    favorites = UserFavorite.objects.filter(user=request.user).select_related('remedy__problem__category')
    return render(request, 'remedies/favorites.html', {'favorites': favorites})

def search_remedies(request):
    """Search for remedies"""
    query = request.GET.get('q', '')
    remedies = []
    
    if query:
        remedies = Remedy.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(problem__name__icontains=query)
        ).distinct()
    
    context = {
        'query': query,
        'remedies': remedies,
    }
    return render(request, 'remedies/search_results.html', context)

@login_required
def ai_consultation(request):
    """AI-powered custom remedy suggestions"""
    if request.method == 'POST':
        problem_description = request.POST.get('problem_description')
        available_ingredients = request.POST.get('available_ingredients')
        
        if problem_description and available_ingredients:
            # Generate AI remedy
            ai_remedy = generate_ai_remedy(problem_description, available_ingredients, request.user)
            parsed_remedy = parse_ai_remedy_payload(ai_remedy)

            if parsed_remedy.get('generation_source') == 'unavailable':
                messages.error(
                    request,
                    'Live AI is not available. Set OPENAI_API_KEY and retry to get a real AI-generated response.'
                )
                consultations = AIConsultation.objects.filter(user=request.user)[:5]
                context = {
                    'consultations': consultations,
                    'problem_description': problem_description,
                    'available_ingredients': available_ingredients,
                }
                return render(request, 'remedies/ai_consultation.html', context)
            
            # Save consultation
            consultation = AIConsultation.objects.create(
                user=request.user,
                problem_description=problem_description,
                available_ingredients=available_ingredients,
                suggested_remedy=ai_remedy
            )
            
            messages.success(request, 'AI consultation completed!')
            return redirect('consultation_detail', consultation_id=consultation.id)
        else:
            messages.error(request, 'Please provide both problem description and available ingredients.')
    
    # Get user's previous consultations
    consultations = AIConsultation.objects.filter(user=request.user)[:5]
    
    return render(request, 'remedies/ai_consultation.html', {'consultations': consultations})

@login_required
def consultation_detail(request, consultation_id):
    """View a specific AI consultation"""
    consultation = get_object_or_404(AIConsultation, id=consultation_id, user=request.user)
    ai_remedy = parse_ai_remedy_payload(consultation.suggested_remedy)
    context = {
        'consultation': consultation,
        'ai_remedy': ai_remedy,
    }
    return render(request, 'remedies/consultation_detail.html', context)
