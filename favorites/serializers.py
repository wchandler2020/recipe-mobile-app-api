from rest_framework import serializers
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(source='user_id')
    recipeId = serializers.IntegerField(source='recipe_id')
    cookTime = serializers.CharField(source='cook_time', allow_null=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'userId', 'recipeId', 'title', 'image', 'cookTime', 'servings', 'createdAt']