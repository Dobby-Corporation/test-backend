from random import shuffle

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .models import Test, TestResult, TaskResult
from .services import get_current_test_result
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
        return redirect('tests.start', id=test.id)
    
    current_task = test_result.get_current_task()
    if current_task is None:
        return redirect('tests.finish', id=test.id)

    return render(request, 'test.html', {
        'test': test,
        'task': current_task.task,
        'task_content': current_task.task.get_specified_task(),
    })

@login_required
def finish(request: HttpRequest, id: int):
    test = Test.objects.get(id=id)
    test_result = get_current_test_result(request.user_info, test)
    
    if test_result is None:
        return redirect('tests.start', id=test.id)
    
    return render(request, 'test-finish.html')

def answer(request: HttpRequest, id: int):
    test = Test.objects.get(id=id)
    test_result = get_current_test_result(request.user_info, test)
    
    if test_result is None:
        return redirect('tests.start', id=test.id)

    current_task = test_result.get_current_task()

    if current_task is None:
        return redirect('tests.finish', id=test.id)
    
    current_task.available = False
    current_task.save()
    
    return redirect('tests.show', id=id)
