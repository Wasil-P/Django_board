from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    tags = models.ManyToManyField("Tag", related_name="posts")

    class Meta():
        ordering = ["-title"]

    @property
    def comments_count(self) -> int:
        return self.comments.all().count()

    def __repr__(self):
        return f"Post - {self.title}"

    def __str__(self):
        return self.title


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    username = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"Comment - {len(self.content)}"

    def __str__(self):
        return self.content


class Tag(models.Model):

    name = models.CharField(max_length=20)

    def __repr__(self):
        return f"Tag - {self.name}"

    def __str__(self):
        return self.name