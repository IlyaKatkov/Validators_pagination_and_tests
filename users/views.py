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



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = Pagination

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        password = serializer.validated_data.get('password')
        if password:
            obj.set_password(password)
            obj.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class PaymentListView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('payed_lesson', 'payed_course')
    ordering_fields = ('date_of_payment',)
    pagination_class = Pagination


class SubscriptionAPIView(views.APIView, Pagination):

    def get(self, *args, **kwargs):
        subs = Subscription.objects.filter(user=self.request.user)
        page = self.paginate_queryset(subs, self.request)
        serializer = SubscriptionSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, *args, **kwargs):
        course = self.get_course_or_404(Course, course_id=kwargs.get('pk'))
        subs, _ = Subscription.objects.get_or_create(user=self.request.user, course=course)
        serializer = SubscriptionSerializer(subs)
        response = {
            'results': serializer.data,
            'detail': f'Курс {course.title} сохранен в подписки'
        }
        return Response(response, status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        course = self.get_course_or_404(Course, course_id=kwargs.get('pk'))
        Subscription.objects.filter(user=self.request.user, course=course).delete()
        response = {
            'detail': f'Курс {course.title} удален из подписок',
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