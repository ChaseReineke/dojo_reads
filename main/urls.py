from main.views import add_book_and_review
from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('books', views.books),
    path('add_book', views.add_book),
    path('add_book_and_review', views.add_book_and_review),
    path('books/<int:id>', views.book_info),
    path('add_review', views.add_review),
    path('users/<int:user_id>', views.user_info),
    path('login', views.login),
    path('logout', views.logout),
]