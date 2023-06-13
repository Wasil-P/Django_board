import textwrap

from django.contrib import admin

from .models import Post, Tag, Comments
from django.utils.html import format_html


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title_short", "created", "user", "comments_count", "tags_all"]
    search_fields = ["title", "created"]
    list_filter = ["user", "tags"]
    list_select_related = ["user"]
    actions = ["add_teg_legion", "delete_teg_all"]

    @admin.action(description="Добавить тег legion")
    def add_teg_legion(self, form, queryset):
        tag, _ = Tag.objects.get_or_create(name="legion")
        for obj in queryset:
            obj.tags.add(tag)

    @admin.action(description="Удалить все теги")
    def delete_teg_all(self, form, queryset):
        for obj in queryset:
            obj.tags.clear()


    @admin.display(description="Заголовок")
    def title_short(self, obj: Post):
        if len(obj.title)>15:
            return textwrap.wrap(obj.title, 15)[0] + "..."
        return obj.title

    @admin.display(description="Кол-во комментариев")
    def comments_count(self, obj: Post):
        return obj.comments_count

    @admin.display(description="Теги")
    def tags_all(self, obj: Post):
        tags_all = obj.tags.all().values_list("name", flat=True)
        rest_list = [f"<li>{tag_name}</li>"for tag_name in tags_all]
        return format_html("".join(rest_list))

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["content_short", "username_show", "email_show"]

    @admin.display(description="Cодержание")
    def content_short(self, obj: Comments):
        if len(obj.content)>5:
            return textwrap.wrap(obj.content, 5)[0] + "..."
        return obj.content

    @admin.display(description="Пользователь")
    def username_show(self, obj: Comments):
        return obj.username

    @admin.display(description="Почта")
    def email_show(self, obj: Comments):
        return obj.email
