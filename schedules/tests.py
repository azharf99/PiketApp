from django.test import TestCase
from django.contrib.auth.models import User
from .models import Schedule, Course, Class
from .models import WEEKDAYS, SCHEDULE_TIME
from datetime import datetime

class ScheduleModelTest(TestCase):
    def setUp(self):
        # Create a teacher for the Course model
        self.teacher = User.objects.create_user(username="teacher1", password="password123")
        
        # Create instances of Course and Class
        self.course = Course.objects.create(
            course_name="Mathematics",
            course_code="MATH101",
            teacher=self.teacher
        )
        self.class_instance = Class.objects.create(
            class_name="Grade 10",
            short_class_name="G10"
        )
        
        # Create a Schedule instance
        self.schedule = Schedule.objects.create(
            schedule_day=0,  # Monday (Senin)
            schedule_time=1,  # Jam ke-1
            schedule_course=self.course,
            schedule_class=self.class_instance
        )

    def test_schedule_creation(self):
        """Test that a Schedule instance is created successfully."""
        self.assertIsInstance(self.schedule, Schedule)
        self.assertEqual(self.schedule.schedule_day, 0)
        self.assertEqual(self.schedule.schedule_time, 1)
        self.assertEqual(self.schedule.schedule_course, self.course)
        self.assertEqual(self.schedule.schedule_class, self.class_instance)

    def test_schedule_day_choices(self):
        """Test that schedule_day respects the defined WEEKDAYS choices."""
        field = Schedule._meta.get_field("schedule_day")
        self.assertEqual(field.choices, [*WEEKDAYS])

    def test_schedule_time_choices(self):
        """Test that schedule_time respects the defined SCHEDULE_TIME choices."""
        field = Schedule._meta.get_field("schedule_time")
        self.assertEqual(field.choices, [*SCHEDULE_TIME])

    def test_schedule_day_max_length(self):
        """Test that schedule_day respects the max_length."""
        max_length = Schedule._meta.get_field("schedule_day").max_length
        self.assertEqual(max_length, 10)

    def test_schedule_time_max_length(self):
        """Test that schedule_time respects the max_length."""
        max_length = Schedule._meta.get_field("schedule_time").max_length
        self.assertEqual(max_length, 20)

    def test_schedule_course_relationship(self):
        """Test that schedule_course correctly relates to Course."""
        self.assertEqual(self.schedule.schedule_course.course_name, "Mathematics")

    def test_schedule_class_relationship(self):
        """Test that schedule_class correctly relates to Class."""
        self.assertEqual(self.schedule.schedule_class.class_name, "Grade 10")

    def test_on_delete_set_null_schedule_course(self):
        """Test that schedule_course is set to null when the related Course is deleted."""
        self.course.delete()
        self.schedule.refresh_from_db()
        self.assertIsNone(self.schedule.schedule_course)

    def test_on_delete_set_null_schedule_class(self):
        """Test that schedule_class is set to null when the related Class is deleted."""
        self.class_instance.delete()
        self.schedule.refresh_from_db()
        self.assertIsNone(self.schedule.schedule_class)

    def test_created_at_auto_now_add(self):
        """Test that created_at is automatically set on instance creation."""
        self.assertIsNotNone(self.schedule.created_at)
        self.assertTrue(isinstance(self.schedule.created_at, datetime))

    def test_updated_at_auto_now(self):
        """Test that updated_at is automatically updated on instance save."""
        old_updated_at = self.schedule.updated_at
        
        # Ensure a delay to allow timestamp to change
        from time import sleep
        sleep(1)

        self.schedule.schedule_day = 1  # Change to Tuesday (Selasa)
        self.schedule.save()

        self.schedule.refresh_from_db()
        new_updated_at = self.schedule.updated_at

        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertTrue(new_updated_at > old_updated_at)
