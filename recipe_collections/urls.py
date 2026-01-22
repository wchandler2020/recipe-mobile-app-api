from django.urls import path
from .views import (
    RecipeCollectionListCreateView,
    RecipeCollectionDetailView,
    AddRecipeView,
    RemoveRecipeView,
)

urlpatterns = [
    # List all collections for user & Create new collection
    path('recipe_collections/',
         RecipeCollectionListCreateView.as_view(),
         name='recipe-collection-list'),

    # Get, Update, or Delete a specific collection
    path('recipe_collections/<int:pk>/',
         RecipeCollectionDetailView.as_view(),
         name='recipe-collection-detail'),

    # Add a recipe to a collection
    path('recipe_collections/<int:pk>/add_recipe/',
         AddRecipeView.as_view(),
         name='add-recipe'),

    # Remove a recipe from a collection
    path('recipe_collections/<int:pk>/remove_recipe/',
         RemoveRecipeView.as_view(),
         name='remove-recipe'),
]



