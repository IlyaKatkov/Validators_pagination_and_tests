from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views, apps

app_name = apps.UsersConfig.name


urlpatterns = [
    path('payment/', views.PaymentListView.as_view(), name='payments'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('subs/', views.SubscriptionAPIView.as_view(), name='sub-list'),
    path('subs/<int:pk>/', views.SubscriptionAPIView.as_view(), name='sub-create-delete')
]