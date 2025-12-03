from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Author, Book, Genre, Publisher, Review  
from .serializers import (
    AuthorSerializer, 
    BookSerializer, 
    UserRegisterSerializer, 
    UserLoginSerializer,
    GenreSerializer,
    PublisherSerializer,
    ReviewSerializer
)


@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "success": True,
            "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi!",
            "data": serializer.data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)
    
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.user 
        
        if user:
            refresh = RefreshToken.for_user(user) 
            
            return Response({
                "success": True,
                "message": "Foydalanuvchi muvaffaqiyatli tizimga kirdi!",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "message": "Not'g'ri foydalanuvchi nomi yoki parol!"
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def jwt_refresh(request):
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response({"detail": "Refresh token talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        refresh = RefreshToken(refresh_token)
        return Response({"access": str(refresh.access_token)})
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])
def author_create(request):

    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Muallif muvaffaqiyatli yaratildi!", "data": serializer.data},
                        status=status.HTTP_201_CREATED)
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@cache_page(60 * 5)
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])
def author_detail(request, pk=None):
    if pk:
        try:
            author = Author.objects.get(pk=pk)
            serializer = AuthorSerializer(author)
            return Response({"success": True, "message": f"Muallif (ID: {pk}) topildi!", "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response({"success": False, "message": f"«{pk}» ID li muallif topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    else:
        queryset = Author.objects.all().order_by('last_name') 
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = AuthorSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['PUT', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def author_update(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response({"success": False, "message": "Muallif topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    serializer = AuthorSerializer(author, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Muallif muvaffaqiyatli yangilandi!", "data": serializer.data},
                        status=status.HTTP_200_OK)
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def author_delete(request, pk):
    try:
        author = Author.objects.get(pk=pk)
        author.delete()
        return Response({"success": True, "message": f"«{pk}» ID li muallif o'chirildi!"}, status=status.HTTP_204_NO_CONTENT)
    except Author.DoesNotExist:
        return Response({"success": False, "message": "Muallif topilmadi!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_create(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Kitob muvaffaqiyatli qo'shildi!", "data": serializer.data},
                        status=status.HTTP_201_CREATED)
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@cache_page(60 * 5)
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_detail(request, pk=None):
    if pk:
        try:
            book = Book.objects.select_related('author').get(pk=pk)
            serializer = BookSerializer(book)
            return Response({"success": True, "message": f"«{book.title}» kitobi topildi!", "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"success": False, "message": f"«{pk}» ID li kitob topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    else:
        queryset = Book.objects.select_related('author').all().order_by('title')
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = BookSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['PUT', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_update(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({"success": False, "message": "Kitob topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    serializer = BookSerializer(book, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Kitob muvaffaqiyatli yangilandi!", "data": serializer.data},
                        status=status.HTTP_200_OK)
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_delete(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        title = book.title
        book.delete()
        return Response({"success": True, "message": f"«{title}» kitobi o'chirildi!"}, status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response({"success": False, "message": "Kitob topilmadi!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def genre_create(request):
    serializer = GenreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Janr muvaffaqiyatli yaratildi!", "data": serializer.data},
                        status=status.HTTP_201_CREATED)
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def genre_detail(request, pk=None):
    if pk:
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response({"success": True, "message": f"«{genre.name}» (ID: {pk}) topildi!", "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Genre.DoesNotExist:
            return Response({"success": False, "message": f"«{pk}» ID li janr topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    else:
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def genre_update(request, pk):
    try:
        genre = Genre.objects.get(pk=pk)
    except Genre.DoesNotExist:
        return Response({"success": False, "message": "Janr topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    serializer = GenreSerializer(genre, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Janr muvaffaqiyatli yangilandi!", "data": serializer.data},
                        status=status.HTTP_200_OK)
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def genre_delete(request, pk):
    try:
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response({"success": True, "message": f"«{pk}» ID li janr o'chirildi!"}, status=status.HTTP_204_NO_CONTENT)
    except Genre.DoesNotExist:
        return Response({"success": False, "message": "Janr topilmadi!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def publisher_create(request):
    serializer = PublisherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Nashriyot muvaffaqiyatli yaratildi!", "data": serializer.data},
                        status=status.HTTP_201_CREATED)
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def publisher_detail(request, pk=None):
    if pk:
        try:
            publisher = Publisher.objects.get(pk=pk)
            serializer = PublisherSerializer(publisher)
            return Response({"success": True, "message": f"«{publisher.name}» (ID: {pk}) topildi!", "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Publisher.DoesNotExist:
            return Response({"success": False, "message": f"«{pk}» ID li nashriyot topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    else:
        queryset = Publisher.objects.all()
        serializer = PublisherSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def publisher_update(request, pk):
    try:
        publisher = Publisher.objects.get(pk=pk)
    except Publisher.DoesNotExist:
        return Response({"success": False, "message": "Nashriyot topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    serializer = PublisherSerializer(publisher, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Nashriyot muvaffaqiyatli yangilandi!", "data": serializer.data},
                        status=status.HTTP_200_OK)
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def publisher_delete(request, pk):
    try:
        publisher = Publisher.objects.get(pk=pk)
        publisher.delete()
        return Response({"success": True, "message": f"«{pk}» ID li nashriyot o'chirildi!"}, status=status.HTTP_204_NO_CONTENT)
    except Publisher.DoesNotExist:
        return Response({"success": False, "message": "Nashriyot topilmadi!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def review_create(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Sharh muvaffaqiyatli qo'shildi!", "data": serializer.data},
                        status=status.HTTP_201_CREATED)
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def review_detail(request, pk=None):
    if pk:
        try:
            review = Review.objects.select_related('book').get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response({"success": True, "message": f"Sharh (ID: {pk}) topildi!", "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({"success": False, "message": f"«{pk}» ID li sharh topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    else:
        queryset = Review.objects.select_related('book').all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def review_update(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response({"success": False, "message": "Sharh topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ReviewSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Sharh muvaffaqiyatli yangilandi!", "data": serializer.data},
                        status=status.HTTP_200_OK)
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated]) 
def review_delete(request, pk):
    try:
        review = Review.objects.get(pk=pk)
        review.delete()
        return Response({"success": True, "message": f"«{pk}» ID li sharh o'chirildi!"}, status=status.HTTP_204_NO_CONTENT)
    except Review.DoesNotExist:
        return Response({"success": False, "message": "Sharh topilmadi!"}, status=status.HTTP_404_NOT_FOUND)