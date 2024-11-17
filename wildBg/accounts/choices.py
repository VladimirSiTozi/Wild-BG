from django.db import models


class UserLevelChoices(models.TextChoices):
    BEGINNER = 'Beginner', 'Beginner'
    INTERMEDIATE = 'Intermediate', 'Intermediate'
    PROFESSIONAL = 'Professional', 'Professional'
    EXPERT = 'Expert', 'Expert'

