from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ("title", "description")
	list_filter = ("title",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
	list_display = ("course", "title", "description", "video_link")
	list_filter = ("course",)
