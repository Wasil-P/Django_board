from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Post


def home(request):

    posts = Post.objects.all()
    return render(request, "todolist/home.html", {"posts": posts})


def create_post(request):
    errors = []
    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("text")

        if not title or not content:
            errors.append("Укажите заголовок и содержимое ")

        else:
            post = Post(
                title=title,
                content=content,)
            post.save()
            return redirect(reverse("post_show", kwargs={"post_id": post.id}))

    return render(request, "todolist/create_post.html", {"errors": errors})


def show_post(request, post_id: int):

    post = get_object_or_404(Post, id=post_id)
    return render(request, "todolist/show_post.html", {"post": post})


def edit_post(request, post_id: int):

    post = get_object_or_404(Post, id=post_id)
    errors = []

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("text")

        post.title = title
        post.content = content

        if not title or not content:
            errors.append("Укажите заголовок и содержимое ")

        else:
            post.save()

            return redirect(reverse("post_show", kwargs={"post_id": post_id}))

    return render(request, "todolist/edit_post.html", {"errors": errors, "post": post})


def delete_post(request, post_id: int):

    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
    else:
        return render(request, "todolist/show_post.html", {"post": post})

    return render(request, "todolist/delete.html", {"post": post})