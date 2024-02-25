from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from users.models import Payments, User, Subscription
from users.serializers import PaymentSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from materials.models import Course
from rest_framework import views
from materials.paginators import Pagination
from rest_framework.permissions import IsAuthenticated
from materials.permissions import IsOwner

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        new_user = serializer.save()
        password = serializer.data["password"]
        new_user.set_password(password)
        new_user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        new_user = serializer.save()
        password = serializer.data["password"]
        new_user.set_password(password)
        new_user.save()


class PaymentListView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('payed_lesson', 'payed_course')
    ordering_fields = ('date_of_payment',)
    pagination_class = Pagination


class SubscriptionAPIView(views.APIView, Pagination):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data["course"]
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user).filter(course=course_id).all()

        if len(subs_item) > 0:
            subscription_id = subs_item[0].pk
            subscription = Subscription.objects.get(pk=subscription_id)
            subscription.delete()
            message = 'Подписка удалена'
        else:
            new_subscription = {
                "user": user,
                "course_id": course_id
            }
            Subscription.objects.create(**new_subscription)
            message = 'Подписка создана'
        return Response({"message": message})

