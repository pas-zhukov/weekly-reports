from datetime import datetime, date
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction

from .serializers import ReportSerializer


@transaction.atomic
@api_view(['POST'])
def submit_report(request):
    reformatted_report = reformat_report_json(request.headers, request.data)
    serializer = ReportSerializer(data=reformatted_report)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, 201)
    else:
        pprint(serializer.errors)
        return Response(str(serializer.errors), 400)


def reformat_report_json(headers: dict, data: dict) -> dict:
    for key, value in data.items():
        if value == "Нет ответа":
            data[key] = ""
    reformatted_report = {
        'date': datetime.strptime(headers['Date'], '%d.%m.%Y'),
        'intern': {
            'name': data['ФИО'],
            'group': {
                'number': int(data['Укажи номер группы.'])
            }
        },
        'department': data['Курс кандидата в какой отдел ты проходишь?'],
        'current_state': data['Над чем сейчас работаешь?'],
        'courses_count': data['Сколько теор. курсов у тебя сейчас в работе?'] if data['Сколько теор. курсов у тебя сейчас в работе?'] else 0,
        'tasks_count': data['Сколько практич. задач у тебя сейчас в работе?'] if data['Сколько практич. задач у тебя сейчас в работе?'] else 0,
        'courses': [
            {
                'course': {
                    'title': data[f'Укажи название курса #{course_number}']
                },
                'custom_title': data[f'Уточни название курса #{course_number}'],
                'start_date': data[f'Дата начала прохождения курса #{course_number}'],
                'is_finished': True if data[f'Я закончил(а) прохождение курса #{course_number}'] == 'Да' else False,
                'end_date': data[f'Дата завершения курса #{course_number}'] if data[f'Дата завершения курса #{course_number}'] else None,
            } if data[f'Укажи название курса #{course_number}'] else None
            for course_number in range(1, 3 + 1)
        ],
        'other_courses': data['Информация об остальных курсах'],
        'tasks': [
            {
                'task': {
                    'title': data[f'Укажи название практической задачи #{task_number}']
                },
                'custom_title': data[f'Уточни название практической задачи #{task_number}'],
                'start_date': data[f'Дата начала работы над задачей #{task_number}'],
                'is_finished': True if data[f'Я завершил(а) задачу #{task_number}'] == 'Да' else False,
                'end_date': data[f'Дата завершения работы над задачей #{task_number}'] if data[f'Дата завершения работы над задачей #{task_number}'] else None,
            } if data[f'Укажи название практической задачи #{task_number}'] else None
            for task_number in range(1, 3 + 1)
        ],
        'projects': [
            {
                'project': {
                    'title': data['Укажи название проекта']
                },
                'custom_title': data['Уточни название проекта'],
                'start_date': data['Дата начала работы над проектом'],
                'comments': data['Информация']
            } if data['Укажи название проекта'] else None
        ],
        'time_spent': data['Укажи суммарно затраченное на работу время.'],
        'progress_comment': data['Напиши в подробностях о прогрессе по работе.'],
        'next_week_url': data['Укажи ссылку на курс/задачу, над которой планируешь работать на следующей неделе.'],
        'difficulties': data['Опиши трудности, возникшие в течение недели, и пути их решения.'],
        'additional_comment': data['Можешь написать здесь любой вопрос, который тебя тревожит.']
    }

    return reformatted_report


def get_count(some_stuff):
    count = 0
    for piece in some_stuff:
        if some_stuff['start_date']:
            count += 1
    return count
