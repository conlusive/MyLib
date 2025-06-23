from django.contrib import admin
from .models import Book, Users, Feedback, Author, Comment


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date')
    search_fields = ('title', 'author__name')
    list_filter = ('publish_date',)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin')
    search_fields = ('username', 'email')
    list_filter = ('is_admin',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    fields = ('name', 'biography', 'birth_date')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'created_at')
    search_fields = ('user__username', 'book__title', 'content')
    list_filter = ('created_at',)


admin.site.register(Book, BookAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)

