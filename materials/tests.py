from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from materials.models import Course
from users.models import User


class CourseTestCase(TestCase):
    def setUp(self):
        self.moderator = User.objects.create(email='1@5.com', password='253679')
        group = Group.objects.create(name='moderator')
        self.moderator.groups.add(group)
        self.moderator.save()

        self.user = User.objects.create(email='3@7.com', password='367821')
        self.user.save()

    def test_course_create(self):
        data = {"title": "course_one", "description": "desc_one"}
        url = reverse('materials:course-list')
        self.client.force_login(user=self.moderator)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_destroy(self):
        course = Course.objects.create(title="course_one", description="desc_one", owner=self.user)
        url = reverse('materials:course-detail', kwargs={'pk': course.pk})
        self.client.force_login(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
