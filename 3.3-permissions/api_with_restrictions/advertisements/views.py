from django.contrib.auth import get_user_model
from django.db.models.query import EmptyQuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from advertisements.models import Advertisement, Favorites
from advertisements.serializers import AdvertisementSerializer, UserSerializer, FavoritesSerializer
from .filters import AdvertisementFilter
from .permissions import IsCreatorOrAdmin, IsMakerOrAdmin
from django.db.models import Q


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий для AdvertisementViewSet"""
        if self.request.method in SAFE_METHODS or self.action == "create":
            return (IsAuthenticatedOrReadOnly(),)
        else:
            return (IsCreatorOrAdmin(),)

    def get_queryset(self):
        """Черновики доступны только автору и админу"""
        if self.request.user.is_staff:
            return Advertisement.objects.all()
        elif str(self.request.user) == 'AnonymousUser':
            return Advertisement.objects.exclude(status='DRAFT')
        else:
            return Advertisement.objects.exclude(~Q(creator=self.request.user), Q(status='DRAFT'))


class UserViewSet(ModelViewSet):
    """ViewSet для пользователей."""
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAdminUser]


    # @action(detail=True, methods=['GET', 'PUT', 'PATCH'])
    # def favorites(self, request, *args, **kwargs):
    #     """ Объявления, добавленные пользователем в избранное"""
    #
    #     user = self.get_object()
    #     qs = Favorites.objects.filter(user=user)
    #     serializer = FavoritesSerializer(qs, many=True)
    #     return Response(serializer.data)
    #
    # @action(detail=False, methods=['GET', 'POST'])
    # def favorites_list(self, request, *args, **kwargs):
    #     """ Все объявления, добавленные в избранное разными пользователями"""
    #     qs = Favorites.objects.all().order_by('user_id')
    #     serializer = FavoritesSerializer(qs, many=True)
    #     return Response(serializer.data)

class FavoritesViewSet(ModelViewSet):
    """ViewSet для избранных."""
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def get_permissions(self):
        """Получение прав для действий для FavoritesViewSet"""
        if self.action == "create":
            return (IsAuthenticated(),)
        else:
            return (IsMakerOrAdmin(),)

    def get_queryset(self):
        """Избранное доступно для админа (все объявления)
            и для того пользователя, который добавил в избранное (только те объявления, что добавил)"""
        if self.request.user.is_staff:
            return Favorites.objects.all()
        elif str(self.request.user) == 'AnonymousUser':
            return Favorites.objects.none()
        else:
            return Favorites.objects.filter(user=self.request.user)




