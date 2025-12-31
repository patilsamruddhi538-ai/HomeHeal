"""
URL configuration for home_remedy_ai project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from remedies import views as remedy_views
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home
    path('', remedy_views.home, name='home'),
    
    # Authentication URLs
    path('signup/', account_views.signup_view, name='signup'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('profile/', account_views.profile_view, name='profile'),
    
    # Remedy URLs
    path('categories/', remedy_views.categories_view, name='categories'),
    path('category/<slug:slug>/', remedy_views.category_detail, name='category_detail'),
    path('category/<slug:category_slug>/<slug:problem_slug>/', remedy_views.problem_detail, name='problem_detail'),
    path('remedy/<int:remedy_id>/', remedy_views.remedy_detail, name='remedy_detail'),
    path('remedy/<int:remedy_id>/favorite/', remedy_views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', remedy_views.favorites_view, name='favorites'),
    path('search/', remedy_views.search_remedies, name='search_remedies'),
    
    # AI Consultation URLs
    path('ai-consultation/', remedy_views.ai_consultation, name='ai_consultation'),
    path('consultation/<int:consultation_id>/', remedy_views.consultation_detail, name='consultation_detail'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
