"""Script to update category icons"""
from remedies.models import Category

# Update the icons
Category.objects.filter(name='General Health and Wellness').update(icon='fa-heart-pulse')
Category.objects.filter(name='Mental Health & Stress Relief').update(icon='fa-leaf')
Category.objects.filter(name='Women\'s Health').update(icon='fa-flower')

print("Icons updated successfully!")
print("\nUpdated categories:")
for cat in Category.objects.all():
    print(f"  {cat.name}: {cat.icon}")
