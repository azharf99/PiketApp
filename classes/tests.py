from django.test import TestCase
from datetime import datetime
from .models import Class
import time

class ClassModelTest(TestCase):
    def setUp(self):
        # Setup a sample instance for testing
        self.class_instance = Class.objects.create(
            class_name="Mathematics",
            short_class_name="Math"
        )



    def test_class_creation(self):
        """Test that a Class instance is created successfully."""
        self.assertIsInstance(self.class_instance, Class)
        self.assertEqual(self.class_instance.class_name, "Mathematics")
        self.assertEqual(self.class_instance.short_class_name, "Math")

    def test_class_name_max_length(self):
        """Test that the class_name field respects the max_length."""
        max_length = Class._meta.get_field("class_name").max_length
        self.assertEqual(max_length, 50)

    def test_short_class_name_max_length(self):
        """Test that the short_class_name field respects the max_length."""
        max_length = Class._meta.get_field("short_class_name").max_length
        self.assertEqual(max_length, 20)

    def test_created_at_auto_now_add(self):
        """Test that created_at is automatically set on instance creation."""
        self.assertIsNotNone(self.class_instance.created_at)
        self.assertTrue(isinstance(self.class_instance.created_at, datetime))

    def test_updated_at_auto_now(self):
        """Test that updated_at is automatically updated on instance save."""
        old_updated_at = self.class_instance.updated_at

        # Ensure a delay to allow the timestamp to change
        time.sleep(1)  # Wait 1 second
        self.class_instance.class_name = "Physics"
        self.class_instance.save()

        # Refresh the instance from the database to get the latest value
        self.class_instance.refresh_from_db()
        new_updated_at = self.class_instance.updated_at

        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertTrue(new_updated_at > old_updated_at)
