from django.conf.urls import url
from .views import RegisterApi,CreateSubadminApi,CreateRestaurantApi,CreateDishApi,GetRestaurantApi,GetDishApi,RestaurantDistanceApi,GetSubadminApi
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    url(r'^register', RegisterApi.as_view()),
    url(r'^login$', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^sub_admin', CreateSubadminApi.as_view()),
    url(r'^restaurant', CreateRestaurantApi.as_view()),
    url(r'^get/restaurant', GetRestaurantApi.as_view()),
    url(r'^dish',CreateDishApi.as_view()),
    url(r'^get/dish',GetDishApi.as_view()),
    url(r'^get/sub_admin',GetSubadminApi.as_view()),
    url(r'^distance/restaurant',RestaurantDistanceApi.as_view()),
]
