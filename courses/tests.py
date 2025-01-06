from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from .models import Course

class CourseModelTest(TestCase):
    def setUp(self):
        # Create a sample User instance for testing
        self.teacher = User.objects.create_user(username="teacher1", password="password123")
        
        # Create a Course instance for testing
        self.course_instance = Course.objects.create(
            course_name="Mathematics",
            course_code="MATH101",
            teacher=self.teacher
        )

    def test_course_creation(self):
        """Test that a Course instance is created successfully."""
        self.assertIsInstance(self.course_instance, Course)
        self.assertEqual(self.course_instance.course_name, "Mathematics")
        self.assertEqual(self.course_instance.course_code, "MATH101")
        self.assertEqual(self.course_instance.teacher, self.teacher)

    def test_course_name_max_length(self):
        """Test that the course_name field respects the max_length."""
        max_length = Course._meta.get_field("course_name").max_length
        self.assertEqual(max_length, 50)

    def test_course_code_max_length(self):
        """Test that the course_code field respects the max_length."""
        max_length = Course._meta.get_field("course_code").max_length
        self.assertEqual(max_length, 20)

    def test_teacher_relationship(self):
        """Test the teacher field is correctly related to the User model."""
        self.assertEqual(self.course_instance.teacher.username, "teacher1")
        self.assertEqual(self.course_instance.teacher, self.teacher)

    def test_on_delete_set_null(self):
        """Test that the teacher field is set to null when the User is deleted."""
        self.teacher.delete()
        self.course_instance.refresh_from_db()
        self.assertIsNone(self.course_instance.teacher)

    def test_created_at_auto_now_add(self):
        """Test that created_at is automatically set on instance creation."""
        self.assertIsNotNone(self.course_instance.created_at)
        self.assertTrue(isinstance(self.course_instance.created_at, datetime))

    def test_updated_at_auto_now(self):
        """Test that updated_at is automatically updated on instance save."""
        old_updated_at = self.course_instance.updated_at
        
        # Ensure a delay to allow the timestamp to change
        from time import sleep
        sleep(1)

        self.course_instance.course_name = "Physics"
        self.course_instance.save()

        self.course_instance.refresh_from_db()
        new_updated_at = self.course_instance.updated_at

        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertTrue(new_updated_at > old_updated_at)
