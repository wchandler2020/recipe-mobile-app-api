from rest_framework import generics, status, serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RecipeCollection
from .serializers import RecipeCollectionSerializers


class RecipeCollectionListCreateView(generics.ListCreateAPIView):

    serializer_class = RecipeCollectionSerializers
    def get_queryset(self):
        """Filter collections by authenticated user"""
        user_id = self.request.headers.get('X-User-Id')
        if not user_id:
            return RecipeCollection.objects.none()
        return RecipeCollection.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        """Automatically sets user_id from request header"""
        user_id = self.request.headers.get('X-User-Id')
        if not user_id:
            raise serializers.ValidationError({
                'user_id': 'X-User-Id header is required'
            })
        serializer.save(user_id=user_id)

    def create(self, request, *args, **kwargs):
        """Override to add better error handling"""
        user_id = request.headers.get('X-User-Id')
        if not user_id:
            return Response(
                {'error': 'X-User-Id header is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)


class RecipeCollectionDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = RecipeCollectionSerializers
    lookup_field = "pk"

    def get_queryset(self):
        """Filter collections by authenticated user"""
        user_id = self.request.headers.get('X-User-Id')
        if not user_id:
            return RecipeCollection.objects.none()
        return RecipeCollection.objects.filter(user_id=user_id)


class AddRecipeView(generics.GenericAPIView):

    serializer_class = RecipeCollectionSerializers
    queryset = RecipeCollection.objects.all()
    lookup_field = "pk"

    def get_queryset(self):
        """Filter collections by authenticated user"""
        user_id = self.request.headers.get('X-User-Id')
        if not user_id:
            return RecipeCollection.objects.none()
        return RecipeCollection.objects.filter(user_id=user_id)

    def post(self, request: Request, pk: int) -> Response:
        """Add a recipe to this collection"""
        recipe_collection = self.get_object()
        recipe_id = request.data.get('recipe_id')

        if not recipe_id:
            return Response(
                {'error': 'recipe_id is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        recipe_id = str(recipe_id)

        if recipe_id in recipe_collection.recipe_ids:
            return Response(
                {'message': 'Recipe already in collection'},
                status=status.HTTP_200_OK,
            )

        recipe_collection.recipe_ids.append(recipe_id)
        recipe_collection.save()

        serializer = self.get_serializer(recipe_collection)
        return Response(serializer.data)


class RemoveRecipeView(generics.GenericAPIView):

    serializer_class = RecipeCollectionSerializers
    queryset = RecipeCollection.objects.all()
    lookup_field = "pk"

    def get_queryset(self):
        """Filter collections by authenticated user"""
        user_id = self.request.headers.get('X-User-Id')
        if not user_id:
            return RecipeCollection.objects.none()
        return RecipeCollection.objects.filter(user_id=user_id)

    def post(self, request: Request, pk: int) -> Response:
        """Remove a recipe from this collection"""
        recipe_collection = self.get_object()
        recipe_id = request.data.get('recipe_id')

        if not recipe_id:
            return Response(
                {'error': 'recipe_id is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        recipe_id = str(recipe_id)

        if recipe_id not in recipe_collection.recipe_ids:
            return Response(
                {'error': 'Recipe not in collection'},
                status=status.HTTP_404_NOT_FOUND,
            )

        recipe_collection.recipe_ids.remove(recipe_id)
        recipe_collection.save()

        serializer = self.get_serializer(recipe_collection)
        return Response(serializer.data)


class TestHeaderView(APIView):

    def get(self, request):
        user_id = request.headers.get('X-User-Id')
        return Response({
            'user_id': user_id,
            'all_headers': dict(request.headers),
        })
