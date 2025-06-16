from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
from .models import Author, Category, Book, Loan


class AuthorModelTest(TestCase):
    
    def setUp(self):
        self.author = Author.objects.create(
            name="George Orwell",
            biography="British author and journalist",
            nationality="British"
        )
    
    def test_author_creation(self):
        self.assertEqual(self.author.name, "George Orwell")
        self.assertEqual(self.author.biography, "British author and journalist")
        self.assertEqual(self.author.nationality, "British")
        self.assertTrue(self.author.created_at)
    
    def test_author_str_method(self):
        self.assertEqual(str(self.author), "George Orwell")
    
    def test_author_with_blank_fields(self):
        author = Author.objects.create(name="Anonymous Author")
        self.assertEqual(author.biography, "")
        self.assertEqual(author.nationality, "")
    
    def test_author_name_max_length(self):
        name_field = Author._meta.get_field('name')
        max_length = name_field.max_length
        
        if max_length:
            long_name = "x" * (max_length + 1)
            author = Author(name=long_name)
            with self.assertRaises(ValidationError):
                author.full_clean()


class CategoryModelTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Science Fiction",
            description="Books about futuristic concepts"
        )
    
    def test_category_creation(self):
        self.assertEqual(self.category.name, "Science Fiction")
        self.assertEqual(self.category.description, "Books about futuristic concepts")
        self.assertTrue(self.category.created_at)
    
    def test_category_str_method(self):
        self.assertEqual(str(self.category), "Science Fiction")
    
    def test_category_unique_name(self):
        with self.assertRaises(Exception):
            Category.objects.create(name="Science Fiction")
    
    def test_category_verbose_name_plural(self):
        self.assertEqual(Category._meta.verbose_name_plural, "Categories")


class BookModelTest(TestCase):
    
    def setUp(self):
        self.author = Author.objects.create(name="Isaac Asimov")
        self.category = Category.objects.create(name="Science Fiction")
        self.book = Book.objects.create(
            title="Foundation",
            author=self.author,
            category=self.category,
            pages=244,
            publication_date=date(1951, 5, 1),
            status='available'
        )
    
    def test_book_creation(self):
        self.assertEqual(self.book.title, "Foundation")
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.category, self.category)
        self.assertEqual(self.book.pages, 244)
        self.assertEqual(self.book.status, 'available')
    
    def test_book_str_method(self):
        expected_str = f"{self.book.title} - {self.author.name}"
        self.assertEqual(str(self.book), expected_str)
    
    def test_book_default_status(self):
        book = Book.objects.create(
            title="Test Book",
            author=self.author,
            category=self.category,
            pages=100,
            publication_date=date.today()
        )
        self.assertEqual(book.status, 'available')
    
    def test_book_pages_validation(self):
        book = Book(
            title="Invalid Book",
            author=self.author,
            category=self.category,
            pages=0,
            publication_date=date.today()
        )
        with self.assertRaises(ValidationError):
            book.full_clean()
    
    def test_book_status_choices(self):
        valid_statuses = ['available', 'loaned', 'maintenance']
        for status_choice in valid_statuses:
            book = Book.objects.create(
                title=f"Book {status_choice}",
                author=self.author,
                category=self.category,
                pages=100,
                publication_date=date.today(),
                status=status_choice
            )
            self.assertEqual(book.status, status_choice)


class LoanModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.category = Category.objects.create(name="Test Category")
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            category=self.category,
            pages=100,
            publication_date=date.today()
        )
        self.loan = Loan.objects.create(
            book=self.book,
            borrower_name="John Doe",
            expected_return_date=date.today() + timedelta(days=14)
        )
    
    def test_loan_creation(self):
        self.assertEqual(self.loan.book, self.book)
        self.assertEqual(self.loan.borrower_name, "John Doe")
        self.assertEqual(self.loan.returned, False)
        self.assertTrue(self.loan.loan_date)
    
    def test_loan_str_method(self):
        expected_str = f"{self.book.title} - {self.loan.borrower_name}"
        self.assertEqual(str(self.loan), expected_str)
    
    def test_loan_default_returned_status(self):
        self.assertFalse(self.loan.returned)
        self.assertIsNone(self.loan.actual_return_date)


class AuthorViewSetTest(APITestCase):
    def setUp(self):
        self.author_data = {
            'name': 'J.K. Rowling',
            'biography': 'British author',
            'nationality': 'British'
        }
        self.author = Author.objects.create(**self.author_data)
    
    def test_get_author_list(self):
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_author(self):
        url = reverse('author-list')
        new_author_data = {
            'name': 'Stephen King',
            'biography': 'American author',
            'nationality': 'American'
        }
        response = self.client.post(url, new_author_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
    
    def test_get_author_detail(self):
        url = reverse('author-detail', kwargs={'pk': self.author.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author.name)
    
    def test_update_author(self):
        url = reverse('author-detail', kwargs={'pk': self.author.pk})
        updated_data = {
            'name': 'J.K. Rowling',
            'biography': 'Updated biography',
            'nationality': 'British'
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.biography, 'Updated biography')
    
    def test_delete_author(self):
        """Test deleting an author"""
        url = reverse('author-detail', kwargs={'pk': self.author.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class CategoryViewSetTest(APITestCase):
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Fantasy',
            description='Fantasy books'
        )
    
    def test_get_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_category(self):
        url = reverse('category-list')
        new_category_data = {
            'name': 'Mystery',
            'description': 'Mystery and thriller books'
        }
        response = self.client.post(url, new_category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
    
    def test_create_duplicate_category_name(self):
        url = reverse('category-list')
        duplicate_data = {
            'name': 'Fantasy',
            'description': 'Another fantasy category'
        }
        response = self.client.post(url, duplicate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookViewSetTest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Test Category')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            category=self.category,
            pages=200,
            publication_date=date.today()
        )
    
    def test_get_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_book(self):
        url = reverse('book-list')
        new_book_data = {
            'title': 'New Book',
            'author': self.author.pk,
            'category': self.category.pk,
            'pages': 150,
            'publication_date': date.today().isoformat()
        }
        response = self.client.post(url, new_book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_book_search_by_title(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_book_search_by_author(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Test Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_book_filter_by_category(self):
        url = reverse('book-list')
        response = self.client.get(url, {'category': self.category.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_book_filter_by_status(self):
        url = reverse('book-list')
        response = self.client.get(url, {'status': 'available'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_book_no_results_search(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class LoanViewSetTest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Test Category')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            category=self.category,
            pages=200,
            publication_date=date.today(),
            status='available'
        )
    
    def test_create_loan(self):
        url = reverse('loan-list')
        loan_data = {
            'book': self.book.pk,
            'borrower_name': 'John Doe',
            'expected_return_date': (date.today() + timedelta(days=14)).isoformat()
        }
        response = self.client.post(url, loan_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, 'loaned')
    
    def test_get_loan_list(self):
        Loan.objects.create(
            book=self.book,
            borrower_name='Jane Doe',
            expected_return_date=date.today() + timedelta(days=14)
        )
        
        url = reverse('loan-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_return_book(self):
        loan = Loan.objects.create(
            book=self.book,
            borrower_name='Jane Doe',
            expected_return_date=date.today() + timedelta(days=14)
        )
        self.book.status = 'loaned'
        self.book.save()
        
        url = reverse('loan-return-book', kwargs={'pk': loan.pk})
        return_data = {'return_date': date.today().isoformat()}
        response = self.client.post(url, return_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'book returned')
        
        loan.refresh_from_db()
        self.assertTrue(loan.returned)
        self.assertIsNotNone(loan.actual_return_date)
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, 'available')


class DashboardViewTest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')
        
        self.book1 = Book.objects.create(
            title='Available Book',
            author=self.author,
            category=self.category1,
            pages=200,
            publication_date=date.today(),
            status='available'
        )
        
        self.book2 = Book.objects.create(
            title='Loaned Book',
            author=self.author,
            category=self.category1,
            pages=150,
            publication_date=date.today(),
            status='loaned'
        )
        
        self.book3 = Book.objects.create(
            title='Another Book',
            author=self.author,
            category=self.category2,
            pages=100,
            publication_date=date.today(),
            status='available'
        )
        
        self.loan = Loan.objects.create(
            book=self.book2,
            borrower_name='John Doe',
            expected_return_date=date.today() + timedelta(days=14)
        )
    
    def test_dashboard_stats(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_stats = {
            'total_books': 3,
            'available_books': 2,
            'loaned_books': 1,
            'total_authors': 1,
            'total_categories': 2,
            'active_loans': 1,
        }
        
        for key, value in expected_stats.items():
            self.assertEqual(response.data[key], value)
        
        books_by_category = response.data['books_by_category']
        self.assertEqual(len(books_by_category), 2)
        
        category_counts = {item['name']: item['book_count'] for item in books_by_category}
        self.assertEqual(category_counts['Category 1'], 2)
        self.assertEqual(category_counts['Category 2'], 1)


class ModelConstraintsTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Test Category')
    
    def test_cascade_delete_author(self):
        book = Book.objects.create(
            title='Test Book',
            author=self.author,
            category=self.category,
            pages=100,
            publication_date=date.today()
        )
        
        self.assertEqual(Book.objects.count(), 1)
        self.author.delete()
        self.assertEqual(Book.objects.count(), 0)
    
    def test_cascade_delete_category(self):
        book = Book.objects.create(
            title='Test Book',
            author=self.author,
            category=self.category,
            pages=100,
            publication_date=date.today()
        )
        
        self.assertEqual(Book.objects.count(), 1)
        self.category.delete()
        self.assertEqual(Book.objects.count(), 0)
    
    def test_cascade_delete_book(self):
        book = Book.objects.create(
            title='Test Book',
            author=self.author,
            category=self.category,
            pages=100,
            publication_date=date.today()
        )
        
        loan = Loan.objects.create(
            book=book,
            borrower_name='Test Borrower',
            expected_return_date=date.today() + timedelta(days=14)
        )
        
        self.assertEqual(Loan.objects.count(), 1)
        book.delete()
        self.assertEqual(Loan.objects.count(), 0)