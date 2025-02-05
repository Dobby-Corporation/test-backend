from django.db import models

from users.models import User

# Create your models here.
class Test(models.Model):
    """ Test model """
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)

    def get_latest_version(self) -> 'TestVersion':
        return TestVersion.objects.filter(test=self).order_by('-id').first()

class TestVersion(models.Model):
    """ Test version model """
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def get_tasks(self):
        return Task.objects.filter(test_version=self).all()

class Task(models.Model):
    """ Task model """
    test_version = models.ForeignKey(TestVersion, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=60)

    def get_specified_task(self):
        match self.type:
            case 'quiz':
                return self.get_quiz_task()
            case 'program':
                return self.get_program_task()

    def get_quiz_task(self):
        return QuizTask.objects.filter(task=self).first()

    def get_program_task(self):
        return ProgramTask.objects.filter(task=self).first()


class QuizTask(models.Model):
    """ Quiz task model """
    description = models.CharField(max_length=500)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class ProgramTask(models.Model):
    """ Program task model """
    description = models.CharField(max_length=1000)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class ProgramTaskTestCase(models.Model):
    """ Program task test case model """
    program_task = models.ForeignKey(ProgramTask, on_delete=models.CASCADE)
    input = models.CharField(max_length=1000)
    output = models.CharField(max_length=1000)

class TestResult(models.Model):
    """ Test result model """
    test_version = models.ForeignKey(TestVersion, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='started')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def has_available_task(self) -> bool:
        return TaskResult.objects.filter(test_result=self, available=True).count() > 0

    def get_current_task(self):
        return TaskResult.objects.filter(test_result=self, available=True).first()

class TaskResult(models.Model):
    """ Test result model """
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
