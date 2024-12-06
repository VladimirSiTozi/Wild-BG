from django.db import models


class LandmarkLevelChoices(models.TextChoices):
    EASY = 'Easy', 'Easy'
    MEDIUM = 'Medium', 'Medium'
    HARD = 'Hard', 'Hard'
    EXTRA_HARD = 'Extra Hard', 'Extra Hard'

