from django.db import models
from django.contrib.auth .models import User

# Create your models here.
class Receipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    receipe_name = models.CharField(max_length=100)
    receipe_description = models.TextField()
    receipe_image = models.ImageField(upload_to="receipe")

# 1. One-to-One (OneToOneField)
# What it means: Each item in one model is linked to only one item in another model.
# Example: Each user has only one profile, and each profile belongs to one user.

# 2. Many-to-One (ForeignKey)
# What it means: Multiple items in one model can be linked to a single item in another model.
# Example: Many posts can belong to one author.

# 3. Many-to-Many (ManyToManyField)
# What it means: Multiple items in one model can be linked to multiple items in another model.
# Example: A student can enroll in many courses, and each course can have many students.

# 4. A ForeignKey is a field in a Django model that,
# creates a relationship where many records in one model can be linked to one record in another model.