from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.serializers import ValidationError

from .models import Movie, platform, Review
from .serializers import MovieSerializer, platformSerializer, reviewSerializer, UserRegisterationSerializer
from .permissions import ReviewPermission, IsAdminOrReadOnly
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from api import models
from rest_framework import filters
from rest_framework.pagination import CursorPagination
from .pagination import Customcursor


@api_view(['POST'])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def userregisteration(request):
    if request.method == 'POST':
        serializer = UserRegisterationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors

        return Response(data=data)


class MovieReviewListapiview(generics.ListAPIView):
    serializer_class = reviewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie__name', 'writer__username']
    pagination_class = Customcursor

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(movie=pk)


class MovieReviewCreateapiview(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = reviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = Movie.objects.get(pk=pk)
        writer = self.request.user
        data = Review.objects.filter(movie=movie, writer=writer)
        if data.exists():
            raise ValidationError('You have already reviewd the movie')

        if movie.average_rating == 0:
            movie.average_rating = (movie.average_rating + serializer.validated_data['review_rating'])
        else:
            movie.average_rating = (movie.average_rating + serializer.validated_data['review_rating']) / 2
            movie.total_ratings = movie.total_ratings + 1
            movie.save()

        serializer.save(movie=movie, writer=writer)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(movie=pk)


class ReviewDetailapiview(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = reviewSerializer
    permission_classes = [ReviewPermission, ]


class ReviewALL(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = reviewSerializer
    pagination_class = Customcursor


class Movieav(APIView):
    permission_classes = [IsAdminOrReadOnly, ]

    def get(self, request, format=None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = MovieSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Created Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Moviedetail(APIView):
    permission_classes = [IsAdminOrReadOnly, ]

    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = MovieSerializer(snippet, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        movie = self.get_object(pk)
        movie.delete()
        return Response({'message': 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class platformav(APIView):
    permission_classes = [IsAdminOrReadOnly, ]

    def get(self, request, format=None):
        platforms = platform.objects.all()
        serializer = platformSerializer(platforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = platformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Created Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class platformdetail(APIView):
    permission_classes = [IsAdminOrReadOnly, ]

    def get_object(self, pk):
        try:
            return platform.objects.get(pk=pk)
        except platform.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        platform = self.get_object(pk)
        serializer = platformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        platform = self.get_object(pk)
        serializer = MovieSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        platform = self.get_object(pk)
        platform.delete()
        return Response({'message': 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
