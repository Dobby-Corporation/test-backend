from django.test import TestCase
from .models import Test, TestVersion, Task, QuizTask, ProgramTask, QuizTaskChoice, ProgramTaskTestCase, TestResult, TaskResult
from users.models import User

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
        self.quiz_task = QuizTask.objects.create(task=self.task_quiz, description='Quiz Task Description')
        self.program_task = ProgramTask.objects.create(task=self.task_program, description='Program Task Description')

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

class QuizTaskModelTest(TestCase):
    def setUp(self):
        self.test = Test.objects.create(name='Test 1', description='Test description')
        self.test_version = TestVersion.objects.create(test=self.test, max_score=1)
        self.task = Task.objects.create(test_version=self.test_version, type='quiz', name='Quiz Task', max_score=1)
        self.quiz_task = QuizTask.objects.create(task=self.task, description='Quiz Task Description')
        self.choice_1 = QuizTaskChoice.objects.create(quiz_task=self.quiz_task, name='Choice 1')
        self.choice_2 = QuizTaskChoice.objects.create(quiz_task=self.quiz_task, name='Choice 2')

    def tearDown(self):
        self.test.delete()
        self.test_version.delete()
        self.task.delete()
        self.quiz_task.delete()
        self.choice_1.delete()
        self.choice_2.delete()

    def test_get_choices(self):
        choices = self.quiz_task.get_choices()
        self.assertEqual(len(choices), 2)
        self.assertIn(self.choice_1, choices)
        self.assertIn(self.choice_2, choices)

class ProgramTaskModelTest(TestCase):
    def setUp(self):
        self.test = Test.objects.create(name='Test 1', description='Test description')
        self.test_version = TestVersion.objects.create(test=self.test, max_score=1)
        self.task = Task.objects.create(test_version=self.test_version, type='program', name='Program Task', max_score=1)
        self.program_task = ProgramTask.objects.create(task=self.task, description='Program Task Description')
        self.test_case_1 = ProgramTaskTestCase.objects.create(program_task=self.program_task, input='Input 1', output='Output 1')
        self.test_case_2 = ProgramTaskTestCase.objects.create(program_task=self.program_task, input='Input 2', output='Output 2')

    def tearDown(self):
        self.test.delete()
        self.test_version.delete()
        self.task.delete()
        self.program_task.delete()
        self.test_case_1.delete()
        self.test_case_2.delete()

    def test_get_test_cases(self):
        test_cases = self.program_task.get_test_cases()
        self.assertEqual(len(test_cases), 2)
        self.assertIn(self.test_case_1, test_cases)
        self.assertIn(self.test_case_2, test_cases)

class TestResultModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(tg_id = '123', username='testuser', first_name='Oleg', last_name='Popov')
        self.test = Test.objects.create(name='Test 1', description='Test description')
        self.test_version = TestVersion.objects.create(test=self.test, max_score=1)
        self.task = Task.objects.create(test_version=self.test_version, type='quiz', name='Quiz Task', max_score=1)
        self.test_result = TestResult.objects.create(test_version=self.test_version, user=self.user, status='started', score=0)
        self.task_result_1 = TaskResult.objects.create(task=self.task, test_result=self.test_result, available=True, )
        self.task_result_2 = TaskResult.objects.create(task=self.task, test_result=self.test_result, available=False)
        self.task_result_3 = TaskResult.objects.create(task=self.task, test_result=self.test_result, available=True)

    def tearDown(self):
        self.user.delete()
        self.test.delete()
        self.test_version.delete()
        self.task.delete()
        self.test_result.delete()
        self.task_result_1.delete()
        self.task_result_2.delete()
        self.task_result_3.delete()

    def test_has_available_task(self):
        self.assertTrue(self.test_result.has_available_task())

        self.task_result_1.available = False
        self.task_result_1.save()
        self.task_result_3.available = False
        self.task_result_3.save()

        self.assertFalse(self.test_result.has_available_task())
    
    def test_get_current_task(self):
        current_task = self.test_result.get_current_task()
        self.assertIsNotNone(current_task)
        self.assertEqual(current_task, self.task_result_1)

        self.task_result_1.available = False
        self.task_result_1.save()
        current_task = self.test_result.get_current_task()
        self.assertEqual(current_task, self.task_result_3)

    def test_get_all_task_results(self):
        tasks = self.test_result.get_all_task_results()
        self.assertEqual(len(tasks), 3)
        self.assertIn(self.task_result_1, tasks)
        self.assertIn(self.task_result_2, tasks)
        self.assertIn(self.task_result_3, tasks)