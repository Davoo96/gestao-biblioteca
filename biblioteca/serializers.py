from rest_framework import serializers
from .models import Author, Category, Book, Loan

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'category', 
                 'category_name', 'pages', 'publication_date', 
                 'status', 'created_at']

class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Loan
        fields = ['id', 'book', 'book_title', 'borrower_name', 
                 'loan_date', 'expected_return_date', 'actual_return_date', 
                 'returned']