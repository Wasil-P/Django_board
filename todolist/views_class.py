from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Post
from django.views import View, generic
from django.db.models import Count, Max
from user.models import User as usermodel
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta


class PostsList(generic.ListView):

    template_name = "todolist/home.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.all().\
            select_related("user").\
            annotate(Count("comments")).\
            values("id",  "title", "created", "user__username", "comments__count").order_by("-comments__count")



class ShowPost(View):

    def get(self, request, post_id: int):
        post = get_object_or_404(Post, id=post_id)
        return render(request, "todolist/show_post.html", {"post": post})


class CreatePost(View):

    def get(self, request):
        return render(request, "todolist/create_post.html")

    def post(self, request):

        title = request.POST.get("title")
        content = request.POST.get("text")
        errors = []

        if self.validate_all(title, content) is False:
            errors.append("Укажите заголовок не более 3 символов и содержимое не более 30 символов")
            return render(request, "todolist/create_post.html", {"errors": errors})
        if self.validate_name(title) is False:
            errors.append("Заметка с таким заголовком уже существует")
            return render(request, "todolist/create_post.html", {"errors": errors})

        post = Post(
            title=title,
            content=content)
        post.save()
        return redirect(reverse("post_show", kwargs={"post_id": post.id}))

    def validate_all(self, title, content: str) -> bool:
        return self.validate_title(title) is True and self.validate_content(content) is True

    def validate_title(self, title: str) -> bool:
        return len(title) <= 3

    def validate_content(self, content: str) -> bool:
        return len(content) <= 30

    def validate_name(self, title) -> bool:

        if Post.objects.filter(title=title):
            return False
        return True


class EditPost(View):

    def get(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)

        return render(request, "todolist/edit_post.html", {"post": post})

    def post(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)
        errors = []
        title = request.POST.get("title")
        content = request.POST.get("text")

        post.title = title
        post.content = content
        if not title or not content:
            errors.append("Укажите заголовок и содержимое")
            return render(request, "todolist/edit_post.html", {"errors": errors, "post": post})
        else:
            post.save()
            return redirect(reverse("post_show", kwargs={"post_id": post_id}))


class DeletePost(View):

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return render(request, "todolist/delete.html", {"post": post})


User: usermodel = get_user_model()


class UsersApp(View):

    @staticmethod
    def get_queryset():
        return User.objects\
            .select_related("todolist_post")\
            .annotate(Count("posts"), Max("posts__created"))\
            .values("id", "posts__count", "posts__created__max", "username")\
            .order_by("-posts__count").exclude(posts__count=0)

    def get(self, request):

        list_users = self.get_queryset()
        return render(request, "todolist/users_app.html", {"list_users": list_users})


class Discussion(View):


    @staticmethod
    def get_queryset():
        return Post.objects.all().select_related("todolist_comments", "user")\
    .annotate(Count("comments__content", distinct=True)).values("id", "title", "user__username", "comments__content__count")\
    .filter(comments__created__gte=(datetime.now() - timedelta(hours=12)))\
    .order_by("-comments__content__count").filter(comments__content__count__gt=2)

    def get(self, request):

        list_posts = self.get_queryset()
        return render(request, "todolist/discussion.html", {"list_posts": list_posts})