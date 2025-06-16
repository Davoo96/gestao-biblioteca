from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('authors/', views.author_list, name='authors'),
    path('authors/create/', views.author_create, name='author_create'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('authors/<int:pk>/update/', views.author_update, name='author_update'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),
    
    path('categories/', views.category_list, name='categories'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    path('books/', views.book_list, name='books'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/update/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    path('loans/', views.loan_list, name='loans'),
    path('loans/create/', views.loan_create, name='loan_create'),
    path('loans/<int:pk>/return/', views.loan_return, name='loan_return'),
    
    path('api/dashboard-stats/', views.dashboard_stats_api, name='dashboard_stats_api'),
]