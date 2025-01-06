from datetime import date
from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import Report, Schedule
from classes.models import Class
from courses.models import Course
from .constants import STATUS_CHOICES


# class ReportModelTest(TestCase):
#     def setUp(self):
#         # Create a teacher for the Course model
#         self.teacher = User.objects.create_user(username="teacher1", password="password123")
        
#         # Create substitute teacher
#         self.substitute_teacher = User.objects.create_user(username="sub_teacher", password="password123")
        
#         # Create instances of Course and Class
#         self.course = Course.objects.create(
#             course_name="Mathematics",
#             course_code="MATH101",
#             teacher=self.teacher
#         )
#         self.class_instance = Class.objects.create(
#             class_name="Grade 10",
#             short_class_name="G10"
#         )
        
#         # Create a Schedule instance
#         self.schedule = Schedule.objects.create(
#             schedule_day=0,  # Monday
#             schedule_time=1,  # Jam ke-1
#             schedule_course=self.course,
#             schedule_class=self.class_instance
#         )
        
#         # Create a Report instance
#         self.report = Report.objects.create(
#             report_date=now().date(),
#             report_day="Senin",  # Auto-generated in real use, explicitly set for testing
#             schedule=self.schedule,
#             status="Hadir",
#             subtitute_teacher=self.substitute_teacher
#         )

#     def test_report_creation(self):
#         """Test that a Report instance is created successfully."""
#         self.assertIsInstance(self.report, Report)
#         self.assertEqual(self.report.report_day, "Senin")
#         self.assertEqual(self.report.status, "Hadir")
#         self.assertEqual(self.report.schedule, self.schedule)
#         self.assertEqual(self.report.subtitute_teacher, self.substitute_teacher)

#     def test_report_day_max_length(self):
#         """Test that report_day respects the max_length constraint."""
#         max_length = Report._meta.get_field("report_day").max_length
#         self.assertEqual(max_length, 20)

#     def test_status_choices(self):
#         """Test that the status field respects the defined choices."""
#         field = Report._meta.get_field("status")
#         self.assertEqual(field.choices, STATUS_CHOICES)

#     def test_status_default_value(self):
#         """Test that the default value of status is correctly set."""
#         report = Report.objects.create(
#             report_date=now().date(),
#             schedule=self.schedule
#         )
#         self.assertEqual(report.status, None)

#     def test_schedule_relationship(self):
#         """Test that the schedule field correctly relates to Schedule."""
#         self.assertEqual(self.report.schedule.schedule_day, 0)  # Monday

#     def test_substitute_teacher_relationship(self):
#         """Test that subtitute_teacher correctly relates to User."""
#         self.assertEqual(self.report.subtitute_teacher.username, "sub_teacher")

#     def test_on_delete_set_null_schedule(self):
#         """Test that the schedule field is set to null when the related Schedule is deleted."""
#         self.schedule.delete()
#         self.report.refresh_from_db()
#         self.assertIsNone(self.report.schedule)

#     def test_on_delete_set_null_substitute_teacher(self):
#         """Test that subtitute_teacher is set to null when the related User is deleted."""
#         self.substitute_teacher.delete()
#         self.report.refresh_from_db()
#         self.assertIsNone(self.report.subtitute_teacher)

#     def test_created_at_auto_now_add(self):
#         """Test that created_at is automatically set on instance creation."""
#         self.assertIsNotNone(self.report.created_at)

#     def test_updated_at_auto_now(self):
#         """Test that updated_at is automatically updated on instance save."""
#         old_updated_at = self.report.updated_at
        
#         # Ensure a delay to allow timestamp to change
#         from time import sleep
#         sleep(1)

#         self.report.status = "Izin"
#         self.report.save()

#         self.report.refresh_from_db()
#         new_updated_at = self.report.updated_at

#         self.assertNotEqual(old_updated_at, new_updated_at)
#         self.assertTrue(new_updated_at > old_updated_at)

#     def test_optional_fields(self):
#         """Test that optional fields can be left blank."""
#         report = Report.objects.create(
#             report_date=now().date(),
#             schedule=self.schedule
#         )
#         self.assertEqual(report.report_day, "")
#         self.assertIsNone(report.subtitute_teacher)


class ReportModelTest(TestCase):
    def setUp(self):
        # Create a teacher and substitute teacher
        self.teacher = User.objects.create_user(username="teacher1", password="password123")
        self.substitute_teacher = User.objects.create_user(username="sub_teacher", password="password123")
        
        # Create Course and Class instances
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
        
        # Create a Report instance
        self.report = Report.objects.create(
            report_date=date(2025, 1, 7),  # Example date
            schedule=self.schedule,
            status="Hadir",
            subtitute_teacher=self.substitute_teacher
        )

    def test_report_creation(self):
        """Test that a Report instance is created successfully."""
        self.assertIsInstance(self.report, Report)
        self.assertEqual(self.report.report_date, date(2025, 1, 7))
        self.assertEqual(self.report.schedule, self.schedule)
        self.assertEqual(self.report.status, "Hadir")
        self.assertEqual(self.report.subtitute_teacher, self.substitute_teacher)

    def test_report_day_property(self):
        """Test the report_day property correctly derives the weekday."""
        self.assertEqual(self.report.report_day, "Selasa")  # January 7, 2025 is a Tuesday (Selasa)

    def test_status_choices(self):
        """Test that status respects the defined STATUS_CHOICES."""
        field = Report._meta.get_field("status")
        self.assertEqual(field.choices, [*STATUS_CHOICES])

    def test_schedule_relationship(self):
        """Test that schedule correctly relates to Schedule."""
        self.assertEqual(self.report.schedule.schedule_day, 0)

    def test_substitute_teacher_relationship(self):
        """Test that subtitute_teacher correctly relates to User."""
        self.assertEqual(self.report.subtitute_teacher.username, "sub_teacher")

    def test_on_delete_set_null_schedule(self):
        """Test that schedule is set to null when the related Schedule is deleted."""
        self.schedule.delete()
        self.report.refresh_from_db()
        self.assertIsNone(self.report.schedule)

    def test_on_delete_set_null_substitute_teacher(self):
        """Test that subtitute_teacher is set to null when the related User is deleted."""
        self.substitute_teacher.delete()
        self.report.refresh_from_db()
        self.assertIsNone(self.report.subtitute_teacher)

    def test_string_representation(self):
        """Test the string representation of a Report instance."""
        expected_str = "2025-01-07 | Hadir | {}".format(self.schedule)
        self.assertEqual(str(self.report), expected_str)

    def test_created_at_auto_now_add(self):
        """Test that created_at is automatically set on instance creation."""
        self.assertIsNotNone(self.report.created_at)

    def test_updated_at_auto_now(self):
        """Test that updated_at is automatically updated on instance save."""
        old_updated_at = self.report.updated_at

        # Ensure a delay to allow timestamp to change
        from time import sleep
        sleep(1)

        self.report.status = "Izin"
        self.report.save()

        self.report.refresh_from_db()
        new_updated_at = self.report.updated_at

        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertTrue(new_updated_at > old_updated_at)