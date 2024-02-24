from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from django.http import Http404
from users.models import Payments, User, Subscription
from users.serializers import PaymentSerializer, UserSerializer, SubscriptionSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
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



class SubscriptionDetailAPIView(views.APIView, Pagination):

    def get(self, *args, **kwargs):
        subs = Subscription.objects.filter(user=self.request.user)
        page = self.paginate_queryset(subs, self.request)
        serializer = SubscriptionSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class SubscriptionCreateDeleteAPIView(views.APIView, Pagination):

    def post(self, *args, **kwargs):
        course = self.get_course_or_404(Course, course_id=kwargs.get('pk'))
        subs, _ = Subscription.objects.get_or_create(user=self.request.user, course=course)
        serializer = SubscriptionSerializer(subs)
        response = {
            'results': serializer.data,
            'detail': f'Курс {course.title} сохранён в подписки'
        }
        return Response(response, status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        course = self.get_course_or_404(Course, course_id=kwargs.get('pk'))
        Subscription.objects.filter(user=self.request.user, course=course).delete()
        response = {
            'detail': f'Курс {course.title} удалён из подписок',
        }
        return Response(response, status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_course_or_404(course, course_id):
        try:
            return get_object_or_404(course, id=course_id)
        except (TypeError, ValueError, ValidationError, Http404):
            response = {
                'detail': f'Курс с id-{course_id} не найден'
            }
            raise Http404(response)

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response(exc.args[0], status=404)
        return super().handle_exception(exc)

