from rest_framework import serializers
from materials.models import Course, Lesson
from materials.validators import ValidatorsVideo
from users.models import Subscription



class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [ValidatorsVideo(field='video_link')]

class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    course_subscription = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['name', 'picture', 'description', 'lesson_count', 'lessons', 'course_subscription']

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    def get_course_subscription(self, instance):
        subscription = Subscription.objects.all().filter(course=instance.pk).filter(
            user=self.context.get('request').user.pk)
        if subscription:
            return True
        else:
            return False

    class Meta:
        model = Course
        fields = ['name', 'picture', 'description', 'lesson_count', 'lessons']


