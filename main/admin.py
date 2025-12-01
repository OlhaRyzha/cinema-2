from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from main.models import Movie, Genre, SiteReview
from django.utils.html import format_html
from unfold.contrib.filters.admin import (
    MultipleChoicesDropdownFilter,
    MultipleRelatedDropdownFilter
)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

admin.site.register(SiteReview)

class MovieTabularInline(TabularInline):
    model = Movie
    extra = 0

class ImageFilter(admin.SimpleListFilter):
    title = 'Відсутнє зображення'
    parameter_name = 'filter_is_empty_image'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(image__isnull=True) | queryset.filter(image__exact='')
        if self.value() == 'no':
            return queryset.exclude(image__isnull=True).exclude(image__exact='')
        return queryset

@admin.register(Genre)
class GenreAdmin(ModelAdmin):
    list_display = ['name', 'image_preview']
    search_fields = ['name']
    list_filter = [ImageFilter]
    # readonly_fields = ['image_preview']
    inlines = [MovieTabularInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No Image"

    image_preview.short_description = "Прев'ю зображення"
@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    list_display = ['id', 'name', 'type', 'release_date', 'is_top_five', 'genre', "duration"]
    list_filter = [("type", MultipleChoicesDropdownFilter), 'is_top_five', ("genre", MultipleRelatedDropdownFilter)]
    list_editable = ['is_top_five']
    search_fields = ['name', 'description']
    ordering = ['-release_date']
    # list_per_page = 3
    list_display_links = ["id", "name"]
    list_filter_submit = True

    fieldsets = (
        (None, {
            'fields': ('name', 'type', 'genre', 'release_date', 'duration', 'is_top_five', 'tag', 'rating')
        }),
        ('Опис', {
            'fields': ('description',),
            'classes': ('wide',),
        })
    )

    actions = ['make_top_five']

    def make_top_five(self, request, queryset):
        queryset.update(is_top_five=True)

    make_top_five.short_description = "Позначити обрані фільми як Топ 5"