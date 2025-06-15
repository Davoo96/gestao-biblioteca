from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import Author, Category, Book, Loan
from .serializers import AuthorSerializer, CategorySerializer, BookSerializer, LoanSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.select_related('author', 'category')
        
        search = self.request.query_params.get('search', None)
        category = self.request.query_params.get('category', None)
        status = self.request.query_params.get('status', None)
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(author__name__icontains=search)
            )
        
        if category:
            queryset = queryset.filter(category_id=category)
            
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    
    def perform_create(self, serializer):
        loan = serializer.save()
        loan.book.status = 'loaned'
        loan.book.save()
        
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        loan.returned = True
        loan.actual_return_date = request.data.get('return_date')
        loan.save()
        
        loan.book.status = 'available'
        loan.book.save()
        
        return Response({'status': 'book returned'})

from rest_framework.views import APIView

class DashboardView(APIView):
    def get(self, request):
        stats = {
            'total_books': Book.objects.count(),
            'available_books': Book.objects.filter(status='available').count(),
            'loaned_books': Book.objects.filter(status='loaned').count(),
            'total_authors': Author.objects.count(),
            'total_categories': Category.objects.count(),
            'active_loans': Loan.objects.filter(returned=False).count(),
            'books_by_category': list(
                Category.objects.annotate(
                    book_count=Count('book')
                ).values('name', 'book_count')
            )
        }
        return Response(stats)