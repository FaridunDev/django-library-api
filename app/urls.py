from django.urls import path
from rest_framework.authtoken import views as drf_views
from .views import (
    register_user,
    login_user,
    jwt_refresh, 

    author_detail,
    author_create,
    author_update,
    author_delete,

    book_detail,
    book_create,
    book_update,
    book_delete,
    
    genre_detail,
    genre_create,
    genre_update,
    genre_delete,

    publisher_detail,
    publisher_create,
    publisher_update,
    publisher_delete,

    review_detail,
    review_create,
    review_update,
    review_delete,
)

urlpatterns = [
    path('api-token-auth/', drf_views.obtain_auth_token),

    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('refresh/', jwt_refresh, name='jwt_refresh'), 

    path('authors/create/', author_create, name='author_create'),
    path('authors/', author_detail, name='author_list_detail'),
    path('authors/<int:pk>/update/', author_update, name='author_update'),
    path('authors/<int:pk>/delete/', author_delete, name='author_delete'),
    path('authors/<int:pk>/', author_detail, name='author_detail'),

    path('books/create/', book_create, name='book_create'),
    path('books/', book_detail, name='book_list_detail'),
    path('books/<int:pk>/update/', book_update, name='book_update'),
    path('books/<int:pk>/delete/', book_delete, name='book_delete'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    
    path('genres/create/', genre_create, name='genre_create'),
    path('genres/', genre_detail, name='genre_list_detail'),
    path('genres/<int:pk>/update/', genre_update, name='genre_update'),
    path('genres/<int:pk>/delete/', genre_delete, name='genre_delete'),
    path('genres/<int:pk>/', genre_detail, name='genre_detail'),
    
    path('publishers/create/', publisher_create, name='publisher_create'),
    path('publishers/', publisher_detail, name='publisher_list_detail'),
    path('publishers/<int:pk>/update/', publisher_update, name='publisher_update'),
    path('publishers/<int:pk>/delete/', publisher_delete, name='publisher_delete'),
    path('publishers/<int:pk>/', publisher_detail, name='publisher_detail'),

    path('reviews/create/', review_create, name='review_create'),
    path('reviews/', review_detail, name='review_list_detail'),
    path('reviews/<int:pk>/update/', review_update, name='review_update'),
    path('reviews/<int:pk>/delete/', review_delete, name='review_delete'),
    path('reviews/<int:pk>/', review_detail, name='review_detail'),
]