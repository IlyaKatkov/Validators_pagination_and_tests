
from rest_framework import status
from materials.models import Course, Lesson
from users.models import User
from django.urls import reverse
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, name="testuser", email="testuser@test.com", phone="12479", city="testcity", password='1234567')
        self.course = Course.objects.create(id=7, name="CourseTest1", description="CourseDesc1", user=self.user)
        self.lesson = Lesson.objects.create(id=1, name="LessonTest1", description="Lesson Disc", video_link="youtube.com", course=self.course, user=self.user)

    def test_course_create(self):
        data = {
            "name": "CourseTest 2",
            "description": "CourseDesc2",
            "user": self.user
        }
        responce = self.client.post(
            reverse('materials: course_create'),
            data=data)

        self.assertEquals(
            responce.status_code,
            status.HTTP_201_CREATED
        )

    def test_course_destroy(self):
        responce = self.client.delete(
            reverse('materials: course_delete')
        )

        self.assertEquals(
            responce.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_get_list_lesson(self):
        responce = self.client.get(
            reverse('materials: lesson-list')
        )
        self.assertEquals(responce.status_code,status.HTTP_200_OK)

    def test_create_lesson(self):
        data = {
            "name": "LessonTest2",
            "description": "LessonDisc2",
            "user": self.user,
            "video_link": "youtube.com",
        }
        print(data)
        responce = self.client.post(
            reverse('materials: lesson-create'),
            data=data
        )
        print(responce)
        self.assertEquals(responce.status_code, status.HTTP_201_CREATED)

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        responce = self.client.delete(
            reverse('materials: lesson-delete')
        )
        print(Lesson.objects.all())

        self.assertEquals(responce.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(id=1, email="testuser@test.com", phone="123456", city="Moscow", password='123456')
        self.course = Course.objects.create(id=7, name="CourseTest1", description="CourseDesc1",owner=self.user)

    def test_create_subscription(self):
        data = {"user": self.user.pk, "course": self.course.pk}
        responce = self.client.post(
            reverse('users: sub-create-delete'),
            data=data
        )

        self.assertEquals(responce.status_code,status.HTTP_200_OK)