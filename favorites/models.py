from django.db import models

class Favorite(models.Model):
    user_id = models.CharField(max_length=255)
    recipe_id = models.IntegerField()
    title = models.CharField(max_length=255)
    image = models.TextField()
    cook_time = models.CharField(max_length=100, null=True, blank=True)
    servings = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorites'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_id} - {self.title}"
