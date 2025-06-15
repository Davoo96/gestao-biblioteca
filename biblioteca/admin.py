from django.contrib import admin
from .models import Author, Category, Book, Loan

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'created_at']
    search_fields = ['name', 'nationality']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'author']
    search_fields = ['title', 'author__name']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower_name', 'loan_date', 'returned']
    list_filter = ['returned', 'loan_date']
    search_fields = ['book__title', 'borrower_name']