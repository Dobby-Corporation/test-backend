from django import template

from .. import models

register = template.Library()

@register.filter
def quiz_choices(task: models.Task):
    return models.QuizTaskChoice.objects.filter(quiz_task__task=task).all()

@register.filter
def quiz_correct_choice(task: models.Task):
    return models.QuizTaskChoice.objects.filter(quiz_task__task=task, is_correct=True).first()

@register.filter
def quiz_choice_name(choice: models.QuizTaskChoice) -> str:
    return choice.name
