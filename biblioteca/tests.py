from django.test import TestCase, Client
from django.urls import reverse
from .models import Author, Category, Book, Loan
from datetime import date, timedelta

class BibliotecaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="Autor Teste")
        self.category = Category.objects.create(name="Ficção")
        self.book = Book.objects.create(
            title="Livro Teste",
            author=self.author,
            category=self.category,
            pages=123,
            publication_date="2020-01-01"
        )
        self.loan = Loan.objects.create(
            book=self.book,
            borrower_name="Fulano",
            expected_return_date=date.today() + timedelta(days=7)
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'biblioteca/dashboard.html')

    def test_dashboard_stats_api(self):
        response = self.client.get(reverse('dashboard_stats_api'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_books', response.json())

    def test_author_crud(self):
        # Create
        response = self.client.post(reverse('author_create'), {
            'name': 'Novo Autor',
            'nationality': 'Brasileiro',
            'biography': 'Bio'
        })
        self.assertRedirects(response, reverse('authors'))

        # Read
        response = self.client.get(reverse('author_detail', args=[self.author.id]))
        self.assertEqual(response.status_code, 200)

        # Update
        response = self.client.post(reverse('author_update', args=[self.author.id]), {
            'name': 'Autor Atualizado',
            'nationality': 'Argentina',
            'biography': 'Atualizado'
        })
        self.assertRedirects(response, reverse('author_detail', args=[self.author.id]))

        # Delete
        response = self.client.post(reverse('author_delete', args=[self.author.id]))
        self.assertRedirects(response, reverse('authors'))

    def test_category_crud(self):
        # Create
        response = self.client.post(reverse('category_create'), {
            'name': 'Nova Categoria',
            'description': 'Descrição'
        })
        self.assertRedirects(response, reverse('categories'))

        # Update
        response = self.client.post(reverse('category_update', args=[self.category.id]), {
            'name': 'Categoria Atualizada',
            'description': 'Nova descrição'
        })
        self.assertRedirects(response, reverse('categories'))

        # Delete
        response = self.client.post(reverse('category_delete', args=[self.category.id]))
        self.assertRedirects(response, reverse('categories'))

    def test_book_crud(self):
        # Create
        response = self.client.post(reverse('book_create'), {
            'title': 'Livro Novo',
            'author': self.author.id,
            'category': self.category.id,
            'pages': 200,
            'publication_date': '2021-01-01',
        })
        self.assertRedirects(response, reverse('books'))

        # Update
        response = self.client.post(reverse('book_update', args=[self.book.id]), {
            'title': 'Livro Atualizado',
            'author': self.author.id,
            'category': self.category.id,
            'pages': 150,
            'publication_date': '2022-02-02',
            'status': 'available',
        })
        self.assertRedirects(response, reverse('books'))

        # Delete
        response = self.client.post(reverse('book_delete', args=[self.book.id]))
        self.assertRedirects(response, reverse('books'))

    def test_loan_create_and_return(self):
        # Mark book as available again for loan
        self.book.status = 'available'
        self.book.save()

        # Create loan
        response = self.client.post(reverse('loan_create'), {
            'book': self.book.id,
            'borrower_name': 'Beltrano',
            'loan_date': date.today(),
            'expected_return_date': date.today() + timedelta(days=5),
        })
        self.assertRedirects(response, reverse('loans'))

        # Return loan
        loan = Loan.objects.latest('id')
        response = self.client.post(reverse('loan_return', args=[loan.id]), {
            'return_date': date.today()
        })
        self.assertRedirects(response, reverse('loans'))
