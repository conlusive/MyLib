from django.db import models
from django.contrib.auth.models import User



class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()
    birth_date = models.DateField(blank=True, null=True)
    # email = models.EmailField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(upload_to='books/', null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None


class Users(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')

    def __str__(self):
        return f'{self.name} - {self.email}'



class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'


class UserLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"