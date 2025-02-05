import json

from . import models

def make_version_from_dict(dict_data: dict, test: models.Test) -> models.TestVersion:
    test_version = models.TestVersion.objects.create(test=test)

    for task in dict_data:
        match task['type']:
            case 'quiz':
                models.QuizTask.objects.create(
                    description=task['description'],
                    task=models.Task.objects.create(
                        test_version=test_version,
                        name=task['name']
                    )
                )
            case 'program':
                program_task = models.ProgramTask.objects.create(
                    description=task['description'],
                    task=models.Task.objects.create(
                        test_version=test_version,
                        name=task['name']
                    )
                )

                for test_case in task['testset']:
                    models.ProgramTaskTestCase.objects.create(
                        program_task=program_task,
                        input=test_case['input'],
                        output=test_case['output']
                    )

    return test_version


def make_version_from_json(json_data: str, test: models.Test) -> models.TestVersion:
    return make_version_from_dict(json.loads(json_data), test)