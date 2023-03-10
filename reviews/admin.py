from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):

    title = "Filter by words!"

    parameter_name = "target_word"

    def lookups(self, request, model_admin):
        return [("wow", "Wow"), ("god", "God")]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews


class ReviewEvaluationFilter(admin.SimpleListFilter):

    title = "Filter good and bad reviews."

    parameter_name = "evaluation_status"

    def lookups(self, request, model_admin):
        return [("good", "Good"), ("bad", "Bad")]

    def queryset(self, request, reviews):
        status = self.value()
        if status:
            if status == "good":
                return reviews.filter(rating__gte=3)
            else:
                return reviews.filter(rating__lt=3)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        ReviewEvaluationFilter,
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )

# from django.contrib import admin
# from .models import Review


# class WordFilter(admin.SimpleListFilter):

#     title = "Filter by words!"

#     parameter_name = "potato"

#     def lookups(self, request, model_admin):
#         return [
#             ("good", "Good"),
#             ("great", "Great"),
#             ("awesome", "Awesome"),
#         ]

#     def queryset(self, request, reviews):
#         word = self.value()
#         if word:
#             return reviews.filter(payload__contains=word)
#         else :
#             reviews

# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
    
#     list_display = (
#         "__str__",
#         "payload",
#     )

#     list_filter = (
#         WordFilter,
#         "rating",
#         "user__is_host",
#         "room__category",
#         "room__pet_friendly",
#     )
