
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('favorites.urls')),
    path('api/', include('recipe_collections.urls'))
]
