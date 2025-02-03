from django.db import models

# Create your models here.
class Test(models.Model):
    """ Test model """
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)

class TestVersion(models.Model):
    """ Test version model """
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

class Task(models.Model):
    """ Task model """
    test_version = models.ForeignKey(TestVersion, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)

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
