from django.test import TestCase

from django.test import TestCase
from .models import Test, TestVersion

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

