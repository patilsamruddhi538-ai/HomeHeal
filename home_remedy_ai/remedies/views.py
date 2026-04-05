import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Category, Problem, Remedy, UserFavorite, AIConsultation
from ai_engine.services import generate_ai_chat_reply, parse_ai_remedy_payload


AI_CHAT_CONTEXT_SESSION_KEY = 'ai_chat_context'
AI_CHAT_HISTORY_SESSION_KEY = 'ai_chat_history'
AI_CHAT_CONSULTATION_ID_SESSION_KEY = 'ai_chat_consultation_id'

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
    """Live AI chat consultation."""
    if request.method == 'POST':
        action = request.POST.get('action', 'message')

        if action == 'reset':
            _clear_ai_chat_session(request)
            return JsonResponse({'ok': True})

        if action == 'context':
            problem_description = (request.POST.get('problem_description') or '').strip()
            available_ingredients = (request.POST.get('available_ingredients') or '').strip()
            _set_ai_chat_context(request, problem_description, available_ingredients)
            return JsonResponse({
                'ok': True,
                'context': _get_ai_chat_context(request),
            })

        user_message = (request.POST.get('message') or '').strip()
        if not user_message:
            return JsonResponse({'ok': False, 'error': 'Please enter a message.'}, status=400)

        conversation_context = _get_ai_chat_context(request)
        conversation_history = _get_ai_chat_history(request)

        assistant_payload = generate_ai_chat_reply(
            user_message=user_message,
            conversation_history=conversation_history,
            user=request.user,
            consultation_context=conversation_context,
        )

        assistant_text = assistant_payload.get('reply', '').strip()
        if not assistant_text:
            assistant_text = 'The live AI service did not return a usable reply.'

        conversation_history.append({'role': 'user', 'content': user_message})
        conversation_history.append({'role': 'assistant', 'content': assistant_text})
        conversation_history = conversation_history[-20:]
        _set_ai_chat_history(request, conversation_history)

        consultation = _save_live_chat_consultation(
            user=request.user,
            context=conversation_context,
            history=conversation_history,
            assistant_payload=assistant_payload,
            request=request,
        )

        return JsonResponse({
            'ok': True,
            'assistant': assistant_text,
            'history': conversation_history,
            'consultation_id': consultation.id if consultation else None,
            'assistant_payload': assistant_payload,
        })

    _restore_latest_live_chat_session(request)
    consultations = AIConsultation.objects.filter(user=request.user)[:5]
    context = {
        'consultations': consultations,
        'chat_history': _get_ai_chat_history(request),
        'chat_context': _get_ai_chat_context(request),
    }
    return render(request, 'remedies/ai_consultation.html', context)

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


def _get_ai_chat_context(request):
    context = request.session.get(AI_CHAT_CONTEXT_SESSION_KEY, {})
    return context if isinstance(context, dict) else {}


def _set_ai_chat_context(request, problem_description, available_ingredients):
    request.session[AI_CHAT_CONTEXT_SESSION_KEY] = {
        'problem_description': problem_description,
        'available_ingredients': available_ingredients,
    }
    request.session.modified = True


def _get_ai_chat_history(request):
    history = request.session.get(AI_CHAT_HISTORY_SESSION_KEY, [])
    if not isinstance(history, list):
        return []

    cleaned = []
    for item in history:
        if not isinstance(item, dict):
            continue
        role = str(item.get('role') or '').strip().lower()
        content = str(item.get('content') or '').strip()
        if role in {'user', 'assistant'} and content:
            cleaned.append({'role': role, 'content': content})
    return cleaned


def _set_ai_chat_history(request, history):
    request.session[AI_CHAT_HISTORY_SESSION_KEY] = history
    request.session.modified = True


def _clear_ai_chat_session(request):
    for key in [AI_CHAT_CONTEXT_SESSION_KEY, AI_CHAT_HISTORY_SESSION_KEY, AI_CHAT_CONSULTATION_ID_SESSION_KEY]:
        if key in request.session:
            del request.session[key]
    request.session.modified = True


def _restore_latest_live_chat_session(request):
    if request.session.get(AI_CHAT_CONTEXT_SESSION_KEY) and request.session.get(AI_CHAT_HISTORY_SESSION_KEY):
        return

    latest_consultation = (
        AIConsultation.objects.filter(user=request.user)
        .order_by('-created_at')
        .first()
    )
    if not latest_consultation:
        return

    latest_payload = parse_ai_remedy_payload(latest_consultation.suggested_remedy)
    if latest_payload.get('generation_source') != 'live_chat':
        return

    consultation_context = latest_payload.get('consultation_context') or {
        'problem_description': latest_consultation.problem_description,
        'available_ingredients': latest_consultation.available_ingredients,
    }
    conversation_history = latest_payload.get('conversation') or []

    request.session[AI_CHAT_CONTEXT_SESSION_KEY] = consultation_context
    request.session[AI_CHAT_HISTORY_SESSION_KEY] = conversation_history
    request.session[AI_CHAT_CONSULTATION_ID_SESSION_KEY] = latest_consultation.id
    request.session.modified = True


def _save_live_chat_consultation(user, context, history, assistant_payload, request):
    consultation_id = request.session.get(AI_CHAT_CONSULTATION_ID_SESSION_KEY)
    payload = {
        'title': 'Live AI Consultation Chat',
        'description': 'Conversational live AI consultation.',
        'matched_problem': context.get('problem_description', '')[:120] or 'General Care',
        'ingredients': [context.get('available_ingredients', '')] if context.get('available_ingredients') else [],
        'instructions': [],
        'usage': '',
        'benefits': [],
        'chemicals': '',
        'reactions': '',
        'importance': assistant_payload.get('safety_note', ''),
        'precautions': [],
        'generation_source': 'live_chat',
        'failure_reason': assistant_payload.get('failure_reason', ''),
        'reply': assistant_payload.get('reply', ''),
        'next_question': assistant_payload.get('next_question', ''),
        'safety_note': assistant_payload.get('safety_note', ''),
        'follow_up_needed': assistant_payload.get('follow_up_needed', False),
        'consultation_context': context,
        'conversation': history,
    }

    if consultation_id:
        consultation = AIConsultation.objects.filter(id=consultation_id, user=user).first()
        if consultation:
            consultation.problem_description = context.get('problem_description', consultation.problem_description)
            consultation.available_ingredients = context.get('available_ingredients', consultation.available_ingredients)
            consultation.suggested_remedy = json.dumps(payload)
            consultation.save(update_fields=['problem_description', 'available_ingredients', 'suggested_remedy'])
            request.session[AI_CHAT_CONSULTATION_ID_SESSION_KEY] = consultation.id
            request.session.modified = True
            return consultation

    consultation = AIConsultation.objects.create(
        user=user,
        problem_description=context.get('problem_description', '') or 'Live AI consultation',
        available_ingredients=context.get('available_ingredients', ''),
        suggested_remedy=json.dumps(payload),
    )
    request.session[AI_CHAT_CONSULTATION_ID_SESSION_KEY] = consultation.id
    request.session.modified = True
    return consultation
