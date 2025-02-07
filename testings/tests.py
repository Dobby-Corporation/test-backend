from django.test import TestCase
from .models import Test, TestVersion, Task, QuizTask, ProgramTask


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

class TaskModelTest(TestCase):
    def setUp(self):
        self.test = Test.objects.create(name='Test 1', description='Test description')
        self.test_version = TestVersion.objects.create(test=self.test, max_score=1)
        self.task_quiz = Task.objects.create(test_version=self.test_version, type='quiz', name='Quiz Task', max_score=1)
        self.task_program = Task.objects.create(test_version=self.test_version, type='program', name='Program Task', max_score=1)
        self.quiz_task = QuizTask.objects.create(task=self.task_quiz)
        self.program_task = ProgramTask.objects.create(task=self.task_program)

    def tearDown(self):
        self.test.delete()
        self.test_version.delete()
        self.task_quiz.delete()
        self.task_program.delete()
        self.quiz_task.delete()
        self.program_task.delete()

    def test_get_specified_task(self):
        quiz_task = self.task_quiz.get_specified_task()
        program_task = self.task_program.get_specified_task()
        self.assertEqual(quiz_task, self.quiz_task)
        self.assertEqual(program_task, self.program_task)

