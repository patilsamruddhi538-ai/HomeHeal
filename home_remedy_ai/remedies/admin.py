from django.contrib import admin
from .models import Category, Problem, Remedy, UserFavorite, AIConsultation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'severity', 'created_at']
    list_filter = ['category', 'severity']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Remedy)
class RemedyAdmin(admin.ModelAdmin):
    list_display = ['title', 'problem', 'effectiveness_rating', 'preparation_time', 'created_at']
    list_filter = ['problem__category', 'effectiveness_rating']
    search_fields = ['title', 'description', 'ingredients']
    list_editable = ['effectiveness_rating']

@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'remedy', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'remedy__title']

@admin.register(AIConsultation)
class AIConsultationAdmin(admin.ModelAdmin):
    list_display = ['user', 'problem_description_short', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'problem_description']
    readonly_fields = ['created_at']
    
    def problem_description_short(self, obj):
        return obj.problem_description[:50] + '...' if len(obj.problem_description) > 50 else obj.problem_description
    problem_description_short.short_description = 'Problem'
