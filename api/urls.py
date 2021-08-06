from django.urls import path
from .views import Movieav, Moviedetail, platformav, platformdetail, MovieReviewListapiview, ReviewDetailapiview, \
    MovieReviewCreateapiview,userregisteration,logout_view,ReviewALL
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('platform/', platformav.as_view(), name='platform'),
    path('platform/<int:pk>/', platformdetail.as_view(), name='platform-detail'),

    path('', Movieav.as_view(), name='movie'),
    path('movie/<int:pk>/', Moviedetail.as_view(), name='movie-detail'),

    # endpoint for particular movie reviews
    path('<int:pk>/review/', MovieReviewListapiview.as_view(), name='movie-review-list'),
    # for creating reviews
    path('<int:pk>/review-create/', MovieReviewCreateapiview.as_view(), name='review'),
    # for detailing review
    path('review/<int:pk>/', ReviewDetailapiview.as_view(), name='review-detail'),
    #endpoint for accessing all reviews
    path('reviews/', ReviewALL.as_view(), name='review-all'),

    path('accounts/login/', obtain_auth_token),
    path('accounts/logout/', logout_view),

    path('accounts/register/', userregisteration,name='registeration'),


]
