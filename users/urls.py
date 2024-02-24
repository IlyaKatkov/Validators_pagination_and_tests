from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views, apps
from users.views import SubscriptionDetailAPIView, SubscriptionCreateDeleteAPIView

app_name = apps.UsersConfig.name


urlpatterns = [
    path('payment/', views.PaymentListView.as_view(), name='payments'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', views.UserCreateAPIView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user_update'),
    path('subs/', SubscriptionDetailAPIView.as_view(), name='sub-detail'),
    path('subs/<int:pk>/', SubscriptionCreateDeleteAPIView.as_view(), name='sub-create-delete')
]

