# Generated by Django 5.1.3 on 2024-11-19 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrecpies', '0010_alter_recipe_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.CharField(choices=[('VEG', 'Vegetarian'), ('NON_VEG', 'Non-Vegetarian'), ('DESSERT', 'Dessert'), ('BEVERAGE', 'Beverage'), ('SNACK', 'Snack'), ('SEAFOOD', 'Seafood'), ('SALAD', 'Salad'), ('SOUP', 'Soup'), ('BREAD', 'Bread'), ('PASTA', 'Pasta'), ('GRILL', 'Grill'), ('RICE', 'Rice'), ('BREAKFAST', 'Breakfast'), ('APPETIZER', 'Appetizer'), ('MAIN_COURSE', 'Main Course'), ('ICE_CREAM', 'Ice Cream'), ('SWEET', 'Sweet'), ('VEGAN', 'Vegan'), ('GLUTEN_FREE', 'Gluten-Free'), ('KIDS_MEAL', 'Kids Meal'), ('FINGER_FOOD', 'Finger Food')], default='VEG', max_length=100),
        ),
    ]
