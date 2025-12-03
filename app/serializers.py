from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Author, Book, Genre, Publisher, Review


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        validate_password(attrs['password'])
        return attrs

    def validate_email(self,value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Faqat '@gmail.com' bilan tugaydigan elektron pochta manzillariga ruxsat beriladi.")
            
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ushbu elektron pochta manzili allaqachon ro'yxatdan o'tgan.")
            
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user = None 

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            self.user = user
            return data
        raise serializers.ValidationError("Kiritilgan ma'lumotlarga mos foydalanuvchi topilmadi.")


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'bio', 'birth_date', 'death_date'] 
        extra_kwargs = {
            'last_name': {'required': True},
            'bio': {'required': False, 'allow_blank': True},
            'birth_date': {'required': False, 'allow_null': True},
            'death_date': {'required': False, 'allow_null': True},
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all(), allow_null=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    author_detail = AuthorSerializer(source='author', read_only=True)
    publisher_detail = PublisherSerializer(source='publisher', read_only=True)
    genres_list = GenreSerializer(source='genres', many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 
            'author', 'author_detail',  
            'publisher', 'publisher_detail', 
            'genres', 'genres_list', 
            'published_date', 'isbn', 'pages', 'description'
        ]
        extra_kwargs = {
            'title': {'required': True},
            'published_date': {'required': False, 'allow_null': True},
        }
        
    def validate_author(self, value):
        if Book.objects.filter(author=value).exists():
            if self.instance and self.instance.author == value:
                return value
            
            raise serializers.ValidationError(
                "Bu muallif (Author) allaqachon bitta kitob yozgan. Har bir muallif faqat bitta kitob yarata oladi."
            )
            
        return value


class ReviewSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    book_title = serializers.CharField(source='book.title', read_only=True)
    

    rating = serializers.IntegerField(min_value=1, max_value=5) 
    
    class Meta:
        model = Review
        fields = [
            'id', 'book', 'book_title', 
            'reviewer_name', 'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['created_at']