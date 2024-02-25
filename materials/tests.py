from rest_framework import status
from materials.models import Course, Lesson
from users.models import User
from rest_framework.test import APITestCase

class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, email="testuser@test.com", phone="12479", city="testcity", password='1234567')
        self.course = Course.objects.create(id=1, name="CourseTest1", description="CourseDesc1", owner=self.user)
        self.lesson = Lesson.objects.create(id=2, name="LessonTest1", description="LessonDesc1", video_link="youtube.com", course=self.course, owner=self.user)

    def test_get_list_course(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            '/courses/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
    def test_create_course(self):
        data = {
            "name": "CourseTest1",
            "description": "CourseDescription1",
            "owner": self.user
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/courses/',
            data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_course_destroy(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            '/courses/1/')

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_get_list_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            '/lesson/')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_lesson(self):
        data = {
            "name": "LessonTest4",
            "description": "LessonDisc2",
            "owner": self.user,
            "video_link": "youtube.com",
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/lesson/create/',
            data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            '/lesson/delete/2/')
        print(Lesson.objects.all())

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionAPITest(APITestCase):
    def setUp(self):
         self.user = User.objects.create(id=1, email="testuser@test.com", phone="123456", city="Moscow", password='123456')
         self.course = Course.objects.create(id=7, name="CourseTest2", description="CourseDesc2", owner=self.user)

    def test_create_subscription(self):
        data = {
            "user": self.user.pk,
            "course": self.course.pk
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/subscription/',
            data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )