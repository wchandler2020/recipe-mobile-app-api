from rest_framework import serializers
from .models import RecipeCollection


class RecipeCollectionSerializers(serializers.ModelSerializer):
    recipe_count = serializers.ReadOnlyField()

    class Meta:
        model = RecipeCollection
        fields = ['id', 'user_id', 'name', 'description', 'recipe_ids',
                  'recipe_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user_id', 'created_at', 'updated_at', 'recipe_count']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Collection name cannot be empty")
        return value.strip()
