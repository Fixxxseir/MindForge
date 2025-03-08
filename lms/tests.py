from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

	def setUp(self) -> None:
		self.user = User.objects.create(email="unit@tester.pro", username="best_tester", password="tester1")
		self.client.force_authenticate(user=self.user)
		self.course = Course.objects.create(title="Курс по DRF", owner=self.user)
		self.lesson = Lesson.objects.create(
			course=self.course,
			title="Урок по DRF",
			video_link="https://www.youtube.com/watch?v=Vg13S-zzol0",
			owner=self.user,
		)

	def test_lesson_retrieve(self):
		"""Тестирование детального просмотра урока"""

		url = reverse("lms:lesson-detail", args=(self.lesson.pk,))
		response = self.client.get(url)

		data = response.json()

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(data.get("title"), self.lesson.title)
		self.assertEqual(data.get("owner"), self.user.pk)

	def test_lesson_create(self):
		"""Тестирование создания урока"""

		url = reverse("lms:lesson-create")
		data = {"title": "Лекция drf", "description": "Введение"}

		response = self.client.post(url, data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Lesson.objects.all().count(), 2)

	def test_lesson_update(self):
		"""Тестирование обновление урока"""
		url = reverse("lms:lesson-update", args=(self.lesson.pk,))

		data = {
			"title": "Урок по Golang",
		}

		response = self.client.patch(url, data)
		data_response = response.json()

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(data_response.get("title"), "Урок по Golang")

	def test_lesson_delete(self):
		"""Тестирование удаление урока"""
		url = reverse("lms:lesson-destroy", args=(self.lesson.pk,))

		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Lesson.objects.all().count(), 0)

	def test_lesson_list(self):
		"""Тестирование создания урока"""
		url = reverse("lms:lesson-list")

		response = self.client.get(url)
		response_data = response.json()

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# current_timezone = timezone.get_current_timezone()
		# time_create_local = self.lesson.time_create.astimezone(current_timezone).isoformat()
		# time_update_local = self.lesson.time_update.astimezone(current_timezone).isoformat()
		for item in response_data["results"]:
			item.pop("time_create", None)
			item.pop("time_update", None)

		result = {
			"count": 1,
			"next": None,
			"previous": None,
			"results": [
				{
					"id": self.lesson.pk,
					"course": self.course.title,
					"title": self.lesson.title,
					"description": None,
					"image_preview": None,
					"video_link": self.lesson.video_link,
					# "time_create": time_create_local,
					# "time_update": time_update_local,
					"owner": self.user.pk,
				}
			],
		}

		self.assertEqual(response.json(), result)
		self.assertEqual(response_data["count"], result["count"])

	def test_lesson_validation_video_link(self) -> None:
		url = reverse("lms:lesson-create")
		data = {"title": "Лекция JAVAAAA", "video_link": "https://www.bobrtube.com/watch?v=bobrdobr"}

		response = self.client.post(url, data)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		self.assertEqual(response.json().get("video_link"), ["Сторонние ресурсы кроме youtube.com запрещены"])


# self.assertEqual(response.json().get('non_field_errors'), ['Сторонние ресурсы кроме youtube.com запрещены'])


class CourseTestCase(APITestCase):

	def setUp(self) -> None:
		self.user = User.objects.create(email="course@tester.pro", username="test_course", password="tester2")
		self.client.force_authenticate(user=self.user)
		self.course = Course.objects.create(title="Курс по Golang", owner=self.user)
		self.lesson = Lesson.objects.create(
			course=self.course,
			title="Урок по DRF",
			video_link="https://www.youtube.com/watch?v=36YnV9STBqc",
			owner=self.user,
		)

	def test_course_retrieve(self):
		"""Тестирование детального просмотра курса"""

		url = reverse("lms:courses-detail", args=(self.course.pk,))
		response = self.client.get(url)

		data = response.json()

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(data.get("title"), self.course.title)
		self.assertEqual(data.get("owner"), self.user.pk)

	def test_course_create(self):
		"""Тестирование создания курса"""

		url = reverse("lms:courses-list")
		data = {"title": "Курс по ДРФ2", "description": "Описание2"}

		response = self.client.post(url, data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Course.objects.all().count(), 2)

	def test_course_update(self):
		"""Тестирование обновление курса"""
		url = reverse("lms:courses-detail", args=(self.course.pk,))

		data = {
			"title": "Курс по Golangggggggggg",
		}

		response = self.client.patch(url, data)
		data_response = response.json()

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(data_response.get("title"), "Курс по Golangggggggggg")

	def test_lesson_delete(self):
		"""Тестирование удаление курса"""
		url = reverse("lms:courses-detail", args=(self.course.pk,))

		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Course.objects.all().count(), 0)

	def test_course_list(self):
		"""Тестирование создания урока"""
		url = reverse("lms:courses-list")

		response = self.client.get(url)
		response_data = response.json()
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		for course in response_data["results"]:
			course.pop("time_create", None)
			course.pop("time_update", None)
			for lesson in course.get("lessons", []):
				lesson.pop("time_create", None)
				lesson.pop("time_update", None)

		result = {
			"count": 1,
			"next": None,
			"previous": None,
			"results": [
				{
					"id": self.course.pk,
					"title": self.course.title,
					"description": None,
					"image_preview": None,
					"owner": self.user.pk,
					"lessons_count": Lesson.objects.count(),
					"lessons": [
						{
							"id": self.lesson.pk,
							"course": self.course.title,
							"video_link": self.lesson.video_link,
							"title": self.lesson.title,
							"description": None,
							"image_preview": None,
							"owner": self.user.pk,
						}
					],
					"subscription": False,
				}
			],
		}

		self.assertEqual(response.json(), result)


class SubscriptionAPITestCase(APITestCase):

	def setUp(self):
		self.user = User.objects.create(email="sub@tester.pro", username="test_sub", password="tester3")
		self.client.force_authenticate(user=self.user)
		self.course = Course.objects.create(title="Course", owner=self.user)
		# self.subscription = Subscription.objects.create(owner=self.user, course=self.course)

	def test_create_subscription(self):
		url = reverse("lms:course-subscription")
		data = {'course_id': self.course.id}
		response = self.client.post(url, data=data)
		response_data = response.json()
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response_data, {'message': 'подписка добавлена'})

	def test_delete_subscription(self):
		Subscription.objects.create(owner=self.user, course=self.course)
		url = reverse("lms:course-subscription")
		data = {'course_id': self.course.id}
		response = self.client.post(url, data=data)
		response_data = response.json()
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response_data, {'message': 'подписка удалена'})

	def test_creating_subscription_for_nonexistent_course(self):
		url = reverse("lms:course-subscription")
		data = {
			'course_id': 12345
		}

		response = self.client.post(url, data=data)

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
