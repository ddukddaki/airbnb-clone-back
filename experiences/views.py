from django.conf import settings
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, PermissionDenied, NotFound
from rest_framework import status
from .models import Experience, Perk
from .serializers import ExperienceListSerializer, ExperienceDetailSerializer, PerkSerializer
from categories.models import Category
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateExperienceBookingSerializer


class Experiences(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(
            experiences,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("Category Kind should be rooms.")
            except Category.DoesNotExist:
                raise ParseError("Category Not Found.")
            try:
                with transaction.atomic():
                    experience = serializer.save(host=request.user, category=category)
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                    serializer = ExperienceDetailSerializer(experience)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Perk not found.")
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        serializer = ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind != Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("Category Kind should be experiences")
                except Category.DoesNotExist:
                    raise ParseError("Category Not Found.")
            try:
                with transaction.atomic():
                    if category_pk:
                        updated_experience = serializer.save(category=category)
                    else:
                        updated_experience = serializer.save()
                    perks = request.data.get("perks")
                    if perks:
                        experience.perks.clear()
                        for perk_pk in perks:
                            perk = Perk.objects.get(pk=perk_pk)
                            updated_experience.perks.add(perk)
                    serializer = ExperienceDetailSerializer(
                        updated_experience,
                        context={"request": request},
                    )
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Perk not found.")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))  # page query의 값을 가져오고 디폴트는 1
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk=pk)
        serializer = PerkSerializer(
            experience.perks.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class ExperienceBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        booking = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
        )
        serializer = PublicBookingSerializer(
            booking,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            booking = serializer.save(  # post는 정상적으로 진행되는데 실질직인 저장이 안됨 뭐지
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = CreateExperienceBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookingsDetail(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk, booking_pk):
        experience = self.get_object(pk)
        try:
            booking = Booking.objects.get(
                experience=experience,
                kind=Booking.BookingKindChoices.EXPERIENCE,
                pk=booking_pk,
            )
        except Booking.DoesNotExist:
            raise NotFound
        serializer = PublicBookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk, booking_pk):

        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied

        try:
            booking = Booking.objects.get(
                pk=booking_pk,
                experience=experience,
            )
        except Booking.DoesNotExist:
            raise NotFound

        serializer = PublicBookingSerializer(
            booking,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    updated_booking = serializer.save()
                    serializer = PublicBookingSerializer(
                        updated_booking,
                    )
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Check your booking again.")

    def delete(self, request, pk, booking_pk):
        experience = self.get_object(pk)
        try:
            booking = Booking.objects.get(
                pk=booking_pk,
                experience=experience,
            )
        except Booking.DoesNotExist:
            raise NotFound
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# from rest_framework.views import APIView
# from rest_framework.status import HTTP_204_NO_CONTENT
# from rest_framework.exceptions import NotFound
# from rest_framework.response import Response
# from .models import Perk
# from .serializers import PerkSerializer

# class Perks(APIView):

#     def get(self, request):
#         all_perks = Perk.objects.all()
#         serializer = PerkSerializer(all_perks, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PerkSerializer(data=request.data)
#         if serializer.is_valid():
#             perk = serializer.save()
#             return Response(PerkSerializer(perk).data)
#         else:
#             return Response(serializer.errors)


# class PerkDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Perk.objects.get(pk=pk)
#         except Perk.DoesNotExist:
#             raise NotFound

#     def get(self, request, pk):
#         perk = self.get_object(pk)
#         serializer = PerkSerializer(perk)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         perk = self.get_object(pk)
#         serializer = PerkSerializer(perk, data=request.data,
#         partial=True)
#         if serializer.is_valid():
#             updated_perk = serializer.save()
#             return Response(
#                 PerkSerializer(updated_perk).data,
#             )
#         else:
#             return Response(serializer.errors)


#     def delete(self, request, pk):
#         perk = self.get_object(pk)
#         perk.delete()
#         return Response(status=HTTP_204_NO_CONTENT)
