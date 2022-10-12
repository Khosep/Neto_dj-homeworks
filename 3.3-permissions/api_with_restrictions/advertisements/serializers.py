from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Advertisement, Favorites

class DefineAdvertFields(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'creator', 'status']
        read_only_fields = ['title', 'description', 'creator', 'status']


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'created_at', 'status')

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        cur_user = self.context['request'].user.id
        new_status = data.get('status')
        method = self.context['request'].method
        if method in ('PUT', 'PATCH'):
            id_adv = self.instance.id
            prev_status = Advertisement.objects.get(pk=id_adv).status
        count_open_status = len(Advertisement.objects.filter(status='OPEN', creator=cur_user))
        # не больше, чем 10 объявлений со статусом 'OPEN'
        if (new_status == 'OPEN' and count_open_status > 9) \
                                and (method == 'POST' or (method in ('PUT', 'PATCH') and prev_status != 'OPEN')):
            raise ValidationError(['You have reached the limit of open adverts: 10'])
        return data

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


class FavoritesSerializer(serializers.ModelSerializer):
    advert = DefineAdvertFields()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Favorites
        fields = ['id', 'user', 'advert']

    def validate(self, data):
        """Метод для валидации Favorites. Вызывается при создании и обновлении."""

        cur_user_id = self.context['request'].user.id
        advert_id = data.get('advert').get('id')
        creator_id = Advertisement.objects.get(id=advert_id).creator.id
        # нельзя добавить в избранное свое собственное объявление
        if creator_id == cur_user_id:
            raise ValidationError(['The author cannot add own advertisement'])

        status = Advertisement.objects.get(id=advert_id).status
        # нельзя добавить в избранное черновик
        if status == 'DRAFT':
            raise ValidationError(['The draft cannot be added to favorites'])

        return {'user_id': cur_user_id, 'advert_id': advert_id}



