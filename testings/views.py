from random import shuffle

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .models import Test, TestResult, TaskResult
from .services import get_current_test_result
from .services import get_test_results
from users.decorators import login_required

# Create your views here.
def index(request: HttpRequest):
    return render(request, 'tests.html')

@login_required
def tests_list(request: HttpRequest):
    tests = Test.objects.all().order_by('-id')
    return render(request, 'available-tests.html', {
        'tests': tests,
    })

@login_required
def start(request: HttpRequest, id: int):
    test = Test.objects.get(id=id)
    version = test.get_latest_version()

    if version is None:
        return HttpResponse(status=406)

    test_result = get_current_test_result(request.user_info, test)

    if test_result is None:
        print("Creating")
        test_result = TestResult.objects.create(
            test_version=version,
            status='started',
            user=request.user_info,
            score=0
        )

        tasks = list(version.get_tasks())
        shuffle(tasks)

        for task in tasks:
            TaskResult.objects.create(
                test_result=test_result,
                task=task,
                score=0
            )

    return redirect('tests.show', id=test.id)

@login_required
def show(request: HttpRequest, id: int):
    test = Test.objects.get(id=id)
    test_result = get_current_test_result(request.user_info, test)
    
    if test_result is None:
        return redirect('tests.info', id=test.id)
    
    current_task = test_result.get_current_task()
    if current_task is None:
        return redirect('tests.finish', id=test.id)
    current_task = current_task.task
    
    match current_task.type:
        case 'program':
            return render(request, 'test-show.program.html', {
                'test': test,
                'task': current_task,
                'task_content': current_task.get_program_task(),
            })
        case 'quiz':
            print(current_task.get_quiz_task().get_choices())
            return render(request, 'test-show.quiz.html', {
                'test': test,
                'task': current_task,
                'task_content': current_task.get_quiz_task(),
                'choices': current_task.get_quiz_task().get_choices(),
            })

@login_required
def finish(request: HttpRequest, id: int):
    test = Test.objects.get(id=id)
    test_result = get_current_test_result(request.user_info, test)
    
    if test_result is None:
        return redirect('tests.info', id=test.id)

    test_result.status = 'complete'
    test_result.save()
    
    return render(request, 'test-finish.html')

@login_required
def answer(request: HttpRequest, id: int):
    test = Test.objects.get(id=id)
    test_result = get_current_test_result(request.user_info, test)
    
    if test_result is None:
        return redirect('tests.start', id=test.id)

    current_task = test_result.get_current_task()

    if current_task is None:
        return redirect('tests.info', id=test.id)
    
    current_task.available = False
    current_task.save()
    
    current_task = test_result.get_current_task()
    if current_task is None:
        return redirect('tests.finish', id=test.id)

    return redirect('tests.show', id=id)

@login_required
def info(request: HttpRequest, id: int):
    test = Test.objects.get(id=id)
    cur_test_result = get_current_test_result(request.user_info, test)
    test_results = get_test_results(request.user_info, test)

    return render(request, 'test-info.html', {
        'test': test,
        'test_results': test_results,
        'has_cur_test_result': cur_test_result is not None,
    })
