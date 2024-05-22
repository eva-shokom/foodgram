from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    AvatarSerializer, CustomUserSerializer, IngredientSerializer,
    LinkSerializers, RecipeReadSerializer, RecipeShortSerializer,
    RecipeWriteSerializer, SubscribeSerializer, TagSerializer
)
from recipes.models import (
    Favorite, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Subscribe,
    Tag
)


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'me':
            return CustomUserSerializer
        return super().get_serializer_class()

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_name='me',
    )
    def me(self, request, *args, **kwargs):
        """Метод для данных о себе."""
        return super().me(request, *args, **kwargs)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        """Метод для подписки на автора и отписки от него."""
        user = request.user
        author_id = self.kwargs.get('id')
        try:
            author = get_object_or_404(User, id=author_id)
        except Http404:
            return Response(
                {'errors': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Subscribe.objects.filter(user=user, author=author).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.get(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """Метод для просмотра своих подписок."""
        user = request.user
        queryset = User.objects.filter(subscribing__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False,
        methods=['put', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='me/avatar'
    )
    def avatar(self, request, **kwargs):
        """Метод для удаления и изменения аватара пользователя."""
        user = self.request.user
        if request.method == 'PUT':
            serializer = AvatarSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            User.objects.filter(id=user.id).update(avatar=None)
            return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly, AllowAny]
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_to(self, model, user, pk):
        """Метод для добавления рецепта в избранное или в список покупок."""
        if model == Favorite:
            error_message = 'избранное'
        elif model == ShoppingCart:
            error_message = 'список покупок'
        if model.objects.filter(
            user=user, recipe__id=pk
        ).exists():
            return Response(
                {'errors': f'Рецепт уже добавлен в {error_message}!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            recipe = get_object_or_404(Recipe, id=pk)
        except Http404:
            return Response(
                {'errors': 'Рецепт не найден'},
                status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        """Метод для удаления рецепта из избранного или из списка покупок."""
        if model == Favorite:
            error_message = 'избранных рецептов'
        elif model == ShoppingCart:
            error_message = 'покупок'
        try:
            recipe = get_object_or_404(Recipe, id=pk)
        except Http404:
            return Response(
                {'errors': 'Рецепт не найден'},
                status=status.HTTP_404_NOT_FOUND)
        obj = model.objects.filter(user=user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': f'Данного рецепта нет в списке {error_message}!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, **kwargs):
        """Метод для добавления рецепта в избранное и удаления из него."""
        user = request.user
        recipe_id = self.kwargs.get('pk')
        if request.method == 'POST':
            return self.add_to(model=Favorite, user=user, pk=recipe_id)
        elif request.method == 'DELETE':
            return self.delete_from(model=Favorite, user=user, pk=recipe_id)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, **kwargs):
        """Метод для добавления рецепта в список покупок и удаления из него."""
        user = request.user
        recipe_id = self.kwargs.get('pk')
        if request.method == 'POST':
            return self.add_to(model=ShoppingCart, user=user, pk=recipe_id)
        elif request.method == 'DELETE':
            return self.delete_from(
                model=ShoppingCart, user=user, pk=recipe_id)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Метод для скачивания списка покупок."""
        user = request.user
        if not user.shopping_cart.exists():
            return Response(
                {'errors': 'Список покупок пуст'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_list = []
        for ingredient in ingredients:
            shopping_list.append(
                (
                    f'- {ingredient["ingredient__name"]} '
                    f'({ingredient["ingredient__measurement_unit"]}) '
                    f'- {ingredient["amount"]}'
                )
            )
        response = HttpResponse(
            '\n'.join(shopping_list), content_type='text.txt'
        )
        response['Content-Disposition'] = (
            'attachment; filename=shopping_list.txt')
        return response

    @action(
        detail=True,
        methods=['get'],
        permission_classes=[AllowAny],
        url_path='get-link',
        url_name='get-link'
    )
    def get_link(self, request, **kwargs):
        """Метод для получения короткой ссылки на рецепт."""
        full_url = request.META.get('HTTP_REFERER')
        recipe_id = kwargs.get('pk')
        if full_url is None:
            url = reverse('api:recipe-detail', kwargs={'pk': recipe_id})
            full_url = request.build_absolute_uri(url)
        serializer = LinkSerializers(
            data={'full_url': full_url}, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
