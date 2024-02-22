from rest_framework import serializers
from materials.models import Course, Lesson
from materials.validators import ValidatorsVideo



class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


    validators = [ValidatorsVideo(field='video_link')]

class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = ['name', 'picture', 'description', 'lesson_count', 'lessons']


