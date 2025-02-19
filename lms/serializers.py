from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = "__all__"

    def get_course(self, instance):
        return instance.course.title


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "image_preview",
            "time_create",
            "time_update",
            "lessons_count",
            "lessons",
        )
        read_only_fields = ("id",)

    def get_lessons_count(self, instance):
        return instance.lessons.count()


# class CourseSerializer(serializers.Serializer):
# 	id = serializers.IntegerField(read_only=True)
# 	title = serializers.CharField(max_length=255)
# 	image_preview = serializers.ImageField(required=False)
# 	description = serializers.CharField(allow_blank=True, required=False)
# 	time_create = serializers.DateTimeField(read_only=True)
# 	time_update = serializers.DateTimeField(read_only=True)
#
# 	def create(self, validated_data):
# 		""" Словарь validated_data состоит
# 		из всех проверенных данных которые пришли с post запросом """
# 		return Course.objects.create(**validated_data)
#
# 	def update(self, instance, validated_data):
# 		""" Обновление, instance - принимаем объект модели Lesson,
# 		validated_data - словарь проверенных данных который нужно изменить """
# 		instance.title = validated_data.get("title", instance.title)
# 		instance.image_preview = validated_data.get("image_preview", instance.image_preview)
# 		instance.description = validated_data.get("description", instance.description)
# 		instance.time_update = validated_data.get("time_update", instance.time_update)
# 		instance.save()
# 		return instance
#
#
# class LessonSerializer(serializers.Serializer):
# 	id = serializers.IntegerField(read_only=True)
# 	course_id = serializers.IntegerField()
# 	title = serializers.CharField(max_length=255)
# 	description = serializers.CharField()
# 	image_preview = serializers.ImageField(required=False)
# 	video_link = serializers.URLField(required=False)
# 	time_create = serializers.DateTimeField(read_only=True)
# 	time_update = serializers.DateTimeField(read_only=True)
#
# 	def create(self, validated_data):
# 		""" Словарь validated_data состоит
# 		из всех проверенных данных которые пришли с post запросом """
# 		return Lesson.objects.create(**validated_data)
#
# 	def update(self, instance, validated_data):
# 		""" Обновление, instance - принимаем объект модели Lesson,
# 		validated_data - словарь проверенных данных который нужно изменить """
# 		instance.course_id = validated_data.get("course_id", instance.course_id)
# 		instance.title = validated_data.get("title", instance.title)
# 		instance.description = validated_data.get("description", instance.description)
# 		instance.image_preview = validated_data.get("image_preview", instance.image_preview)
# 		instance.video_link = validated_data.get("video_link", instance.video_link)
# 		instance.time_update = validated_data.get("time_update", instance.time_update)
# 		instance.save()
# 		return instance
