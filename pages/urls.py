from django.urls import path
from . import views
from .views import feedback_view
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=False)),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('create/', views.create, name='create'),
    path('feedback/', feedback_view, name='feedback'),
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='pages/logout.html'), name='logout'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('search/', views.search, name='search'),
    path('remove/<int:book_id>/', views.remove_from_library, name='remove_from_library'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



