from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Post
from django.views import View, generic
from django.db.models import Count, Max
from user.models import User as usermodel
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .forms import PostForm, EditProfileForm
from django.db import transaction

class PostsList(generic.ListView):

    template_name = "todolist/home.html"
    context_object_name = "posts"
    paginate_by = 6
    page_kwarg = "page"

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
    model = Post
    def get(self, request):
        return render(request, "todolist/create_post.html", {"form": PostForm()})

    def post(self, request):

        form = PostForm(request.POST)

        if not form.is_valid():
            return render(request, "todolist/create_post.html", {"form": form})

        with transaction.atomic():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            tags = form.cleaned_data["tags"]

            post = self.model.objects.create(
            title=title,
            content=content,
            user=request.user,
            )
            post.tags.add(*list(tags))
            post.save()
        return redirect(reverse("post_show", kwargs={"post_id": post.id}))


class EditPost(View):
    model = Post

    def get(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)

        return render(request, "todolist/edit_post.html", {"post": post, "form":
            PostForm(initial={"title": post.title, "content": post.content})})

    def post(self, request, post_id):

        form = PostForm(request.POST)
        post = get_object_or_404(Post, id=post_id)


        if not form.is_valid():
            return render(request, "todolist/edit_post.html", {"form": form})

        with transaction.atomic():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            tags = form.cleaned_data["tags"]

            post.title = title
            post.content = content
            post.tags.add(*list(tags))

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


class ShowProfile(View):
    model = User

    def get(self, request):
        user = request.user
        return render(request, "user/profile_show.html", {"form_user": EditProfileForm(
            initial={"username": user.username, "email": user.email, "profile_picture": user.profile_picture})})


class EditProfile(View):
    model = User

    def get(self, request):
        user = request.user
        return render(request, "user/edit_user.html", {"form_user": EditProfileForm(
            initial={"username": user.username, "email": user.email, "profile_picture": user.profile_picture})})
    def post(self, request):

        form = EditProfileForm(request.POST)
        user = request.user

        if not form.is_valid():
            return render(request, "user/profile_show.html", {"form_user": form})

        with transaction.atomic():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            profile_picture = form.cleaned_data["profile_picture"]

            user.username = username
            user.email = email
            user.profile_picture = profile_picture

            user.save()
        return redirect(reverse("user/profile_show", kwargs={"form_user": form}))