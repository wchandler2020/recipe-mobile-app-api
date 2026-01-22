from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Favorite
from .serializers import FavoriteSerializer


class HealthCheckView(APIView):
    """Health check"""
    def get(self, request):
        return Response({'success': True}, status=status.HTTP_200_OK)


class FavoriteCreateView(generics.CreateAPIView):
    """Create a new favorite recipe"""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('userId')
            recipe_id = request.data.get('recipeId')
            title = request.data.get('title')

            if not user_id or not recipe_id or not title:
                return Response(
                    {'error': 'Missing required fields'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print('error', e)
            return Response(
                {'error': 'Something went wrong...'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserFavoritesListView(generics.ListAPIView):
    """Gets all favorites for a user"""
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Favorite.objects.filter(user_id=user_id)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print('error', e)
            return Response(
                {'error': 'User not found...'},
                status=status.HTTP_404_NOT_FOUND
            )


class FavoriteDeleteView(generics.DestroyAPIView):
    """Delete a recipe from favorites list"""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = None

    def delete(self, request, *args, **kwargs):
        try:
            user_id = self.kwargs['user_id']
            recipe_id = self.kwargs['recipe_id']

            deleted_count, _ = Favorite.objects.filter(
                user_id=user_id,
                recipe_id=int(recipe_id)
            ).delete()

            return Response(
                {'message': 'Recipe has been removed...'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print('error', e)
            return Response(
                {'error': 'Recipe ID does not exist...'},
                status=status.HTTP_400_BAD_REQUEST
            )