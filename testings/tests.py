from django.test import TestCase
from .models import Test, TestVersion, Task


class TestModelTest(TestCase):
    def setUp(self):
        self.test = Test.objects.create(name='Test 1', description='Test description')
        self.test_version_1 = TestVersion.objects.create(test=self.test, max_score=1)
        self.test_version_2 = TestVersion.objects.create(test=self.test, max_score=2)

    def tearDown(self):
        self.test.delete()
        self.test_version_1.delete()
        self.test_version_2.delete()

    def test_get_latest_version(self):
        latest_version = self.test.get_latest_version()
        self.assertEqual(latest_version, self.test_version_2)

class TestVersionModelTest(TestCase):
    def setUp(self):
        self.test = Test.objects.create(name='Test 1', description='Test description')
        self.test_version = TestVersion.objects.create(test=self.test, max_score=1)
        self.task_1 = Task.objects.create(test_version=self.test_version, name='Task 1')
        self.task_2 = Task.objects.create(test_version=self.test_version, name='Task 2')

    def tearDown(self):
        self.test.delete()
        self.test_version.delete()
        self.task_1.delete()
        self.task_2.delete()

    def test_get_tasks(self):
        tasks = self.test_version.get_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertIn(self.task_1, tasks)
        self.assertIn(self.task_2, tasks)