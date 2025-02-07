import datetime
import json

from pathlib import Path
from subprocess import Popen, PIPE

from django.db.models.fields.files import FieldFile
from django.conf import settings

from files.services import create_file_from_str
from users.models import User
from . import models

def make_version_from_dict(dict_data: dict, test: models.Test) -> models.TestVersion:
    test_version = models.TestVersion.objects.create(test=test)
    test_version.max_score = 0

    for task in dict_data:
        test_version.max_score += task.get('max_score', 1)
        match task['type']:
            case 'quiz':
                quiz_task = models.QuizTask.objects.create(
                    description=task['description'],
                    task=models.Task.objects.create(
                        test_version=test_version,
                        name=task['name'],
                        type=task['type']
                    )
                )

                for choice in range(len(task['choices'])):
                    models.QuizTaskChoice.objects.create(
                        quiz_task=quiz_task,
                        name=task['choices'][choice],
                        is_correct=choice == task['answer']
                    )
                    
            case 'program':
                program_task = models.ProgramTask.objects.create(
                    description=task['description'],
                    task=models.Task.objects.create(
                        test_version=test_version,
                        name=task['name'],
                        type=task['type']
                    )
                )

                for test_case in task['testset']:
                    models.ProgramTaskTestCase.objects.create(
                        program_task=program_task,
                        input=test_case['input'],
                        output=test_case['output']
                    )

    test_version.save()
    return test_version


def make_version_from_json(json_data: str, test: models.Test) -> models.TestVersion:
    test_version = make_version_from_dict(json.loads(json_data), test)
    test_version.config_file = create_file_from_str(json_data, 'config.json', 'application/json')
    test_version.save()
    return test_version

def get_current_test_result(user: User, test: models.Test):
    query = models.TestResult.objects.filter(test_version__test=test, user=user, status='started')
    return query.first()

def get_latest_test_result(user: User, test: models.Test):
    query = models.TestResult.objects.filter(test_version__test=test, user=user, status='started')
    return query.order_by('-id').first()

def get_test_results(user: User, test: models.Test):
    return models.TestResult.objects.filter(user=user, test_version__test=test).order_by('-id').all()

def run(filepath: str, input_data: str) -> str:
    p = Popen(['python3', filepath], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    stdout_data = p.communicate(input_data)[0]
    p.terminate()
    return stdout_data.strip()

def check_program(program_file: FieldFile, task: models.ProgramTask):
    correct_cases = 0
    total_cases = len(task.get_test_cases())

    for test_case in task.get_test_cases():
        input_data = test_case.input
        output_data = test_case.output
        
        if run(program_file.path, input_data) == output_data:
            correct_cases += 1

    return correct_cases / total_cases