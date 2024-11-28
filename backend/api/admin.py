from django.contrib import admin
from django.core.exceptions import ValidationError

from api.models import *


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "min_salary",
        "max_salary",
        "currency",
        "experience",
        "number_of_openings",
        "publication_date",
        "status",
        "format",
        "employment_type",
    )
    search_fields = ("title", "city", "description")
    list_filter = (
        "currency",
        "city",
        "experience",
        "publication_date",
        "status",
        "format",
        "employment_type",
    )
    filter_horizontal = ("tags", "languages")  


    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean() 
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error("number_of_openings", e.messages)



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "candidate_name",
        "desired_position",
        "email",
        "phone",
        "city",
        "updated_at",
    )  
    search_fields = (
        "candidate_name",
        "email",
        "desired_position",
    )  
    list_filter = ("city",)  
    ordering = ("-updated_at",)  
    filter_horizontal = ("languages", "tags")  


admin.site.register(
    Resume, ResumeAdmin
)  


class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)  
    search_fields = ("name",)  



admin.site.register(Language, LanguageAdmin)

@admin.action(description="Загрузить языки в Redis")
def load_languages_to_cache(modeladmin, request, queryset):
    Language.load_to_cache()

@admin.action(description="Загрузить навыки в Redis")
def load_tags_to_cache(modeladmin, request, queryset):
    Tag.load_to_cache()


class LanguageAdmin(admin.ModelAdmin):
    actions = [load_languages_to_cache]


class TagAdmin(admin.ModelAdmin):
    actions = [load_tags_to_cache]