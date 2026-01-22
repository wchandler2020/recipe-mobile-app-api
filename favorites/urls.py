from django.urls import path
from . import views

urlpatterns = [
    path('health', views.HealthCheckView.as_view(), name='health'),
    path('favorites', views.FavoriteCreateView.as_view(), name='create_favorite'),
    path('favorites/<str:user_id>', views.UserFavoritesListView.as_view(), name='get_favorites'),
    path('favorites/<str:user_id>/<int:recipe_id>', views.FavoriteDeleteView.as_view(), name='delete_favorite'),
]