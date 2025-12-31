from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Main categories: Skincare, Body Care, Hair Care"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For Font Awesome icons
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Problem(models.Model):
    """Specific problems within each category"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='problems')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField()
    severity_choices = [
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ]
    severity = models.CharField(max_length=20, choices=severity_choices, default='mild')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']
        unique_together = ['category', 'slug']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Remedy(models.Model):
    """Home remedies for each problem"""
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='remedies')
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField(help_text="List ingredients line by line")
    instructions = models.TextField(help_text="Step by step instructions")
    usage = models.TextField(help_text="How to use and frequency")
    benefits = models.TextField(help_text="Benefits of this remedy")
    chemicals = models.TextField(blank=True, help_text="Active chemical compounds")
    reactions = models.TextField(blank=True, help_text="How chemicals react")
    importance = models.TextField(blank=True, help_text="Why this remedy works")
    precautions = models.TextField(help_text="Warnings and precautions")
    preparation_time = models.CharField(max_length=50, blank=True)
    effectiveness_rating = models.IntegerField(default=5, help_text="Rate 1-10")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Remedies"
        ordering = ['-effectiveness_rating', 'title']

    def __str__(self):
        return self.title

class UserFavorite(models.Model):
    """User's favorite remedies"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    remedy = models.ForeignKey(Remedy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'remedy']

    def __str__(self):
        return f"{self.user.username} - {self.remedy.title}"

class AIConsultation(models.Model):
    """AI-powered custom remedy suggestions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations')
    problem_description = models.TextField()
    available_ingredients = models.TextField(help_text="Products/ingredients available at home")
    suggested_remedy = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"AI Consultation for {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"
