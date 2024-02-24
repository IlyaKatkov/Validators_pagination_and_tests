
from rest_framework import status
from materials.models import Course, Lesson
from users.models import User
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import Group


class CourseTestCase(TestCase):
    def setUp(self):
        self.moderator = User.objects.create(email='1@1.com', password='123123')
        group = Group.objects.create(name='moderator')
        self.moderator.groups.add(group)
        self.moderator.save()

        self.user = User.objects.create(email='2@2.com', password='321123')
        self.user.save()

    def test_course_create(self):
        data = {"title": "course1", "description": "desc1"}
        url = reverse('lms:course-list')
        self.client.force_login(user=self.moderator)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_destroy(self):
        course = Course.objects.create(title="course1", description="desc1", owner=self.user)
        url = reverse('lms:course-detail', kwargs={'pk': course.pk})
        self.client.force_login(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_list_lesson(self):
        self.client.force_authenticate(owner=self.user)
        responce = self.client.get('/lesson/')
        self.assertEquals(responce.status_code,status.HTTP_200_OK)

    def test_create_lesson(self):
        data = {
            "name": "LessonTest2",
            "description": "LessonDiscription2",
            "user": self.user,
            "video_link": "youtube.com",
        }
        print(data)
        self.client.force_authenticate(owner=self.user)
        responce = self.client.post('/course/', data=data)
        print(responce)
        self.assertEquals(responce.status_code, status.HTTP_201_CREATED)

    def test_delete_lesson(self):
        self.client.force_authenticate(owner=self.user)
        responce = self.client.delete('/lesson/delete/1/')
        print(Lesson.objects.all())

        self.assertEquals(responce.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionAPITest(TestCase):

    def setUp(self):
        self.user = User.objects.create(id=1, email="testuser@test.com", phone="123456", city="Moscow", password='123456')
        self.course = Course.objects.create(id=7, name="CourseTest1", description="CourseDescroption1",owner=self.user)

    def test_create_subscription(self):
        data = {"user": self.user.pk, "course": self.course.pk}
        self.client.force_authenticate(user=self.user)
        responce = self.client.post('/subs/', data=data)

        self.assertEquals(responce.status_code,status.HTTP_200_OK)