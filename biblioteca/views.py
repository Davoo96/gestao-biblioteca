from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Author, Category, Book, Loan
from .forms import BookForm, AuthorForm, CategoryForm

def dashboard(request):
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
    return render(request, 'biblioteca/dashboard.html', {'stats': stats})

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'biblioteca/authors/list.html', {'authors': authors})

def author_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        nationality = request.POST.get('nationality', '')
        biography = request.POST.get('biography', '')
        
        if name:
            Author.objects.create(name=name, nationality=nationality, biography=biography)
            messages.success(request, 'Autor criado com sucesso!')
            return redirect('authors')
        else:
            messages.error(request, 'Preciso do nome do autor!')
    
    return render(request, 'biblioteca/authors/create.html')


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author)
    return render(request, 'biblioteca/authors/detail.html', {'author': author, 'books': books})

def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autor atualizado com sucesso!')
            return redirect('author_detail', pk=pk)
    else:
        form = AuthorForm(instance=author)
    
    return render(request, 'biblioteca/authors/update.html', {'form': form})


def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        author.delete()
        messages.success(request, 'Autor removido com sucesso!')
        return redirect('authors')
    
    return render(request, 'biblioteca/authors/delete.html', {'author': author})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'biblioteca/categories/list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            Category.objects.create(name=name, description=description)
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('categories')
        else:
            messages.error(request, 'Preciso de um nome para a categoria!')
    
    return render(request, 'biblioteca/categories/create.html')

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = Book.objects.filter(category=category)
    return render(request, 'biblioteca/categories/detail.html', {'category': category, 'books': books})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'biblioteca/categories/update.html', {'form': form})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoria removida com sucesso!')
        return redirect('categories')
    
    return render(request, 'biblioteca/categories/delete.html', {'category': category})

def book_list(request):
    authors = Author.objects.all()
    books = Book.objects.select_related('author', 'category').all()
    categories = Category.objects.all()
    
    search = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')
    
    if search:
        books = books.filter(
            Q(title__icontains=search) | 
            Q(author__name__icontains=search)
        )
    
    if category_filter:
        books = books.filter(category_id=category_filter)
        
    if status_filter:
        books = books.filter(status=status_filter)
    
    context = {
        'books': books,
        'authors': authors,
        'categories': categories,
        'search': search,
        'category_filter': category_filter,
        'status_filter': status_filter,
    }
    return render(request, 'biblioteca/books/list.html', context)

def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        category_id = request.POST.get('category')
        publication_date = request.POST.get('publication_date')
        pages = request.POST.get('pages')
        
        if title and author_id and category_id:
            Book.objects.create(
                title=title,
                author_id=author_id,
                category_id=category_id,
                publication_date=publication_date or None,
                pages=pages or None,
            )
            messages.success(request, 'Book created successfully!')
            return redirect('books')
        else:
            messages.error(request, 'Title, Author, and Category are required!')
    
    authors = Author.objects.all()
    categories = Category.objects.all()
    return render(request, 'biblioteca/books/create.html', {'authors': authors, 'categories': categories})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    loans = Loan.objects.filter(book=book).order_by('-loan_date')
    return render(request, 'biblioteca/books/detail.html', {'book': book, 'loans': loans})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('books')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'biblioteca/books/update.html', {
        'form': form,
    })

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Livro removido com sucesso!')
        return redirect('books')
    
    return render(request, 'biblioteca/books/delete.html', {'book': book})

def loan_list(request):
    books = Book.objects.filter(status='available')
    loans = Loan.objects.select_related('book', 'book__author').all()
    return render(request, 'biblioteca/loans/list.html', {
        'loans': loans,
        'books': books,
        'today': date.today()
    })

def loan_create(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        borrower_name = request.POST.get('borrower_name')
        loan_date = request.POST.get('loan_date')
        expected_return_date = request.POST.get('expected_return_date')
        
        if book_id and borrower_name:
            book = get_object_or_404(Book, pk=book_id)
            if book.status == 'available':
                Loan.objects.create(
                    book=book,
                    borrower_name=borrower_name,
                    loan_date=loan_date or timezone.now().date(),
                    expected_return_date=expected_return_date
                )
                book.status = 'loaned'
                book.save()
                messages.success(request, 'Livro alugado com sucesso!')
                return redirect('loans')
            else:
                messages.error(request, 'Este livro não esta disponível para alugar!')
        else:
            messages.error(request, 'Preciso dos nomes do livro e pessoa que quer alugar!')
    
    available_books = Book.objects.filter(status='available')
    return render(request, 'biblioteca/loans/create.html', {'books': available_books})

def loan_detail(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    return render(request, 'biblioteca/loans/detail.html', {'loan': loan})

@require_http_methods(["POST"])
def loan_return(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    
    if not loan.returned:
        loan.returned = True
        loan.actual_return_date = request.POST.get('return_date', timezone.now().date())
        loan.save()
        
        loan.book.status = 'available'
        loan.book.save()
        
        messages.success(request, 'Devolução do livro feito com sucesso!')
    else:
        messages.info(request, 'Este livro já foi retornado!')
    
    return redirect('loans')

def dashboard_stats_api(request):
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
    return JsonResponse(stats)
