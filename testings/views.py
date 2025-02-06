from datetime import datetime
from random import shuffle

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Test, TestResult, TaskResult, QuizTaskChoice, ProgramTaskResult, QuizTaskResult
from files.services import create_file_from_str
from .services import get_current_test_result
from .services import get_test_results
from .services import check_program
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

    test_result.completed_at = datetime.now()

    test_result.status = 'complete'
    test_result.save()

    return render(request, 'test-finish.html')

@require_POST
@login_required
def answer(request: HttpRequest, id: int):
    test = Test.objects.get(id=id)
    test_result = get_current_test_result(request.user_info, test)
    
    if test_result is None:
        return redirect('tests.start', id=test.id)

    current_task = test_result.get_current_task()

    if current_task is None:
        return redirect('tests.info', id=test.id)
    
    max_score = current_task.task.max_score
    earned_score = 0
    match current_task.task.type:
        case 'quiz':
            choice = request.POST.get('choice')
            quiz_choice = QuizTaskChoice.objects.filter(quiz_task__task=current_task.task, id=choice).first()

            current_task.quiz_task_result = QuizTaskResult.objects.create(choice=quiz_choice)
            
            if quiz_choice is None:
                return redirect('tests.show', id=id)

            if quiz_choice.is_correct:
                earned_score = current_task.task.max_score

        case 'program':
            program = None
            file = request.FILES.get('program_file')
            if file is not None:
                program = file.read().decode('utf-8')
            else:
                program = request.POST.get('program_text')
            program_file = create_file_from_str(program, 'program.py', 'text/py')
            current_task.program_task_result = ProgramTaskResult.objects.create(program_file=program_file)
            earned_score = check_program(program, current_task.task.get_program_task()) * current_task.task.max_score



    current_task.available = False
    current_task.score = earned_score
    current_task.save()

    test_result.score += earned_score
    test_result.save()

    
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

@login_required
def result(request: HttpRequest, id: int):
    test_result = TestResult.objects.get(id=id)
    task_results = test_result.get_all_task_results()
    return render(request, 'test-result.html', {
        'test_result': test_result,
        'task_results': task_results
    })
