from django.db import models
from django.core.validators import MinLengthValidator

class RecipeCollection(models.Model):
    user_id = models.CharField(max_length=255, db_index=True)
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(1)]
    )
    description = models.TextField(blank=True, null=True)
    recipe_ids = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', '-created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({len(self.recipe_ids)} recipes)"

    @property
    def recipe_count(self):
        return len(self.recipe_ids)
