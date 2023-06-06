from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()

    @property
    def comments_count(self) -> int:
        return self.comments.all().count()


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    username = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
