from django import forms
from .models import Book, Feedback, Comment
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@example.com'):
            raise forms.ValidationError("Email must be from the domain 'example.com'")
        return email

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author Name',
            'content': 'Book Content',
            'image': 'Image',
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea'}),
        }


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Коментар',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
