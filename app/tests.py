from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date 
# Model validatsiyasi uchun qo'shildi
from django.core.exceptions import ValidationError 


from .models import Author, Book, Genre, Publisher, Review
from .serializers import AuthorSerializer, BookSerializer, GenreSerializer, PublisherSerializer, ReviewSerializer


# =============================
# 1. MODEL TESTS
# =============================
class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="Alisher",
            last_name="Karimov",
            bio="Taniqli dramaturg",
            birth_date=date(1980, 5, 10) 
        )

    def test_author_creation(self):
        self.assertEqual(self.author.first_name, "Alisher")
        self.assertEqual(self.author.last_name, "Karimov")
        self.assertEqual(str(self.author), "Alisher Karimov")
        self.assertEqual(self.author.birth_date, date(1980, 5, 10))


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="Test", last_name="Author")
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.genre = Genre.objects.create(name="Test Genre")

        self.book = Book.objects.create(
            title="Test Kitob",
            author=self.author,
            publisher=self.publisher,
            isbn="1234567890123",
            pages=300
        )
        self.book.genres.add(self.genre)

    def test_book_relationships(self):
        self.assertEqual(self.book.author.last_name, "Author")
        self.assertEqual(self.book.publisher.name, "Test Publisher")
        self.assertTrue(self.book.genres.filter(name="Test Genre").exists())


class ReviewModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(last_name="A")
        self.book = Book.objects.create(title="Kitob", author=self.author)
        self.review = Review.objects.create(
            book=self.book,
            reviewer_name="User",
            rating=4
        )
    
    def test_review_rating_validation(self):
        # 0 reytingni tekshirish
        review_low = Review(book=self.book, reviewer_name="Test Low", rating=0)
        with self.assertRaises(ValidationError):
            review_low.full_clean()  # Model validatsiyasini majburlash

        # 6 reytingni tekshirish
        review_high = Review(book=self.book, reviewer_name="Test High", rating=6)
        with self.assertRaises(ValidationError):
            review_high.full_clean() # Model validatsiyasini majburlash


# =============================
# 2. SERIALIZER TESTS
# =============================
class AuthorSerializerTest(TestCase):
    def test_author_serializer_fields(self):
        author = Author.objects.create(first_name="T", last_name="Test", birth_date=date(1990, 1, 1))
        serializer = AuthorSerializer(author)
        
        expected_fields = ['id', 'last_name', 'first_name', 'bio', 'birth_date', 'death_date']
        self.assertEqual(sorted(list(serializer.data.keys())), sorted(expected_fields))


# =============================
# 3. API TESTS (CRUD)
# =============================
class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.author = Author.objects.create(first_name="Old", last_name="Author")
        self.publisher = Publisher.objects.create(name="Old Publisher")
        self.genre = Genre.objects.create(name="Old Genre")
        self.book = Book.objects.create(
            title="Old Book", author=self.author, publisher=self.publisher, isbn="9998887776665")
        self.book.genres.add(self.genre)
        self.review = Review.objects.create(book=self.book, reviewer_name="Old User", rating=5)

    def tearDown(self):
        self.client.credentials() 

    def get_urls(self, model_name, pk=None):
        base = model_name.lower()
        if pk:
            return {
                'detail': reverse(f'{base}_detail', kwargs={'pk': pk}),
                'update': reverse(f'{base}_update', kwargs={'pk': pk}),
                'delete': reverse(f'{base}_delete', kwargs={'pk': pk}),
            }
        return {
            'list': reverse(f'{base}_list_detail'),
            'create': reverse(f'{base}_create'),
        }


class AuthorAPITest(BaseAPITestCase):
    def test_author_create(self):
        url = self.get_urls('Author')['create']
        data = {'first_name': 'New', 'last_name': 'Author', 'bio': 'A writer'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_author_list(self):
        url = self.get_urls('Author')['list']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1) 

    def test_author_update(self):
        url = self.get_urls('Author', self.author.pk)['update']
        update_data = {'last_name': 'Updated Name'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.last_name, 'Updated Name')

    def test_author_delete(self):
        url = self.get_urls('Author', self.author.pk)['delete']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class BookAPITest(BaseAPITestCase):
    def test_book_create(self):
        url = self.get_urls('Book')['create']
        data = {
            'title': 'New Book', 
            'author': self.author.pk, 
            'publisher': self.publisher.pk, 
            'genres': [self.genre.pk]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_book_update(self):
        url = self.get_urls('Book', self.book.pk)['update']
        update_data = {'title': 'Updated Title', 'pages': 500}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')


class GenreAPITest(BaseAPITestCase):
    def test_genre_create(self):
        url = self.get_urls('Genre')['create']
        data = {'name': 'New Genre'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)

    def test_genre_update(self):
        url = self.get_urls('Genre', self.genre.pk)['update']
        update_data = {'name': 'Updated Genre'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.genre.refresh_from_db()
        self.assertEqual(self.genre.name, 'Updated Genre')


class PublisherAPITest(BaseAPITestCase):
    def test_publisher_create(self):
        url = self.get_urls('Publisher')['create']
        data = {'name': 'New Publisher', 'address': 'Tashkent'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Publisher.objects.count(), 2)

    def test_publisher_delete(self):
        url = self.get_urls('Publisher', self.publisher.pk)['delete']
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Publisher.objects.count(), 0)


class ReviewAPITest(BaseAPITestCase):
    def test_review_create(self):
        url = self.get_urls('Review')['create']
        data = {'book': self.book.pk, 'reviewer_name': 'New Reviewer', 'rating': 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)

    def test_review_invalid_rating(self):
        url = self.get_urls('Review')['create']
        data = {'book': self.book.pk, 'reviewer_name': 'Bad Rater', 'rating': 6}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rating', response.data['errors'])

    def test_review_delete_unauthenticated(self):
        url = self.get_urls('Review', self.review.pk)['delete']
        self.client.credentials() 
        self.client.force_authenticate(user=None)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)