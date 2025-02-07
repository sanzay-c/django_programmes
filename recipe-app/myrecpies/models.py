from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Recipe(models.Model):
    # this added if something wrong delete this.
    CATEGORY_CHOICES = [
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
        ('DESSERT', 'Dessert'),
        ('BEVERAGE', 'Beverage'),
        ('SNACK', 'Snack'),
        ('SEAFOOD', 'Seafood'),
        ('SALAD', 'Salad'),
        ('SOUP', 'Soup'),
        ('BREAD', 'Bread'),
        ('PASTA', 'Pasta'),
        ('GRILL', 'Grill'),
        ('RICE', 'Rice'),
        ('BREAKFAST', 'Breakfast'),
        ('APPETIZER', 'Appetizer'),
        ('MAIN_COURSE', 'Main Course'),
        ('ICE_CREAM', 'Ice Cream'),
        ('SWEET', 'Sweet'),
        ('VEGAN', 'Vegan'),
        ('GLUTEN_FREE', 'Gluten-Free'),
        ('KIDS_MEAL', 'Kids Meal'),
        ('FINGER_FOOD', 'Finger Food'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=100)
    recipe_ingridents = models.CharField(max_length=100)
    recipe_description = models.TextField()
    instructions = models.TextField(default=None)
  
    cooking_time = models.IntegerField(help_text="Cooking time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
  
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES)
    recipe_image = models.ImageField(upload_to="recepie")

    def __str__(self) -> str:
        return self.recipe_name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_name = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    bio = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    needs_update = models.BooleanField(default=True)

    @property
    def following_count(self):
        return self.followers.count()

    def followers_count(self):
        return self.user.following.count()
    
# Create your models here.
