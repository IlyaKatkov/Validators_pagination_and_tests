from rest_framework import serializers
from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


# class MotoSerializer(serializers.ModelSerializer):
#     last_milage = serializers.SerializerMethodField
#
#     class Meta:
#         model = Moto
#         fields = '__all__'
#
#
#     def get_last_milage(self, instance):
#         if instance.milage.all().first():
#             return instance.milage.all().first().milage
#         return 0
#
#
#
# class MotoMilageSerializer(serializers.ModelSerializer):
#     moto = MotoSerializer
#
#     class Meta:
#         model = Milage
#         fields = ('milage', 'year', 'moto')
#
#
# class MotoCreateSerializer(serializers.ModelSerializer):
#     milage = MilageSerializer(many=True)
#
#     class Meta:
#         model = Moto
#         fields = '__all__'
#
#     def create(self, validated_data):
#         milage = validated_data.pop('milage')
#
#         moto_item = Moto.objects.create(**validated_data)
#
#         for m in milage:
#             Milage.objects.create(**m, moto=moto_item)
#
#         return moto_item
#
