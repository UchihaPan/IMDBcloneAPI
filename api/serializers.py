from rest_framework import serializers
from .models import Movie, platform, Review
from django.contrib.auth.models import User


class reviewSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField(read_only=True)
    writer = serializers.StringRelatedField()
    url = serializers.HyperlinkedIdentityField(view_name="review-detail")

    class Meta:
        model = Review
        exclude = ('active',)


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    review = reviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')
    url = serializers.HyperlinkedIdentityField(view_name="movie-detail")

    class Meta:
        model = Movie
        fields = ['url', 'id', 'name', 'description', 'total_ratings', 'average_rating', 'created_at', 'platform',
                  'review']


class platformSerializer(serializers.ModelSerializer):
    movies = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = platform
        fields = ['id', 'name', 'about', 'website', 'movies']


class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'message': 'Please enter correct password'})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'message': 'Email already exists'})

        account = User(username=self.validated_data['username'], email=self.validated_data['email'])
        account.set_password(self.validated_data['password2'])
        account.save()
        return account
