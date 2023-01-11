from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "pk",
            "name",
            "description",
        )


class RoomListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    category = CategorySerializer()

    class Meta:
        model = Room
        fields = (
            "name",
            "pk",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
            "category",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user


class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(
        read_only=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context.get("request")
        if request:
            return room.owner == request.user
        return False

    def get_is_liked(self, room):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Wishlist.objects.filter(
                    user=request.user,
                    rooms__pk=room.pk,
                ).exists()
        return False


class TinyRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "name",
            "price",
        )

# from rest_framework import serializers
# from .models import Amenity, Room
# from users.serializers import TinyUserSerializer
# from reviews.serializers import ReviewSerializer
# from categories.serializers import CategorySerializer
# from medias.serializers import PhotoSerializer
# from wishlists.models import Wishlist


# class AmenitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Amenity
#         fields = (
#             "name",
#             "description",
#         )


# class RoomDetailSerializer(serializers.ModelSerializer):

#     owner = TinyUserSerializer(read_only=True)
#     amenities = AmenitySerializer(
#         read_only=True,
#         many=True,
#     )
#     category = CategorySerializer(
#         read_only=True,
#     )
#     rating = serializers.SerializerMethodField()
#     is_owner = serializers.SerializerMethodField()
#     is_liked = serializers.SerializerMethodField()
#     photos = PhotoSerializer(many=True, read_only=True)

#     class Meta:
#         model = Room
#         fields = "__all__"

#     def get_rating(self, room):
#         return room.rating()

#     def get_is_owner(self, room):
#         request = self.context.get("request")
#         if request:
#             return room.owner == request.user
#         return False
#         # request = self.context["request"]
#         # return room.owner == request.user

#     def get_is_liked(self, room):
#         request = self.context.get("reqeust")
#         if request:
#             if request.user.is_authentication:
#                 return Wishlist.objects.filter(
#                     user=request.use,
#                     rooms__pk=room.pk,
#                 ).exists()
#         return False

#     # def get_is_liked(self, room):
#     #     request = self.context["request"]
#     #     return Wishlist.objects.filter(
#     #         user=request.user.id,
#     #         #user=request.user 로 .id 없이 코딩시 500 에러 발생
#     #         rooms__pk=room.pk,
#     #     ).exists()


# class RoomListSerializer(serializers.ModelSerializer):

#     rating = serializers.SerializerMethodField()
#     is_owner = serializers.SerializerMethodField()
#     photos = PhotoSerializer(many=True, read_only=True)

#     class Meta:
#         model = Room
#         fields = (
#             "pk",
#             "name",
#             "country",
#             "city",
#             "price",
#             "rating",
#             "is_owner",
#             "photos",
#         )

#     def get_rating(self, room):
#         return room.rating()

#     def get_is_owner(self, room):
#         request = self.context["request"]
#         return room.owner == request.user