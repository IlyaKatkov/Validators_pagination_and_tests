from django.db import models
NULLABLE = {'blank': True, 'null': True}

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='название курса')
    description = models.TextField(**NULLABLE, verbose_name='описание курса')
    picture = models.ImageField(upload_to='course/', verbose_name='превью курса', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока')
    picture = models.ImageField(upload_to='lesson_picture/', verbose_name='превью урока', **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='курс')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
