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
    return render(request, 'test.html')