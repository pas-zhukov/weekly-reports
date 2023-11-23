import pprint

from rest_framework.serializers import ModelSerializer, ListField, ValidationError
from rest_framework import serializers

from .models import Group, Intern
from .models import Course, Task, Project
from .models import CourseInProgress, TaskInProgress, ProjectInProgress
from .models import Report


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['number']


class InternSerializer(ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = Intern
        fields = ['name', 'group']


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['title']


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['title']


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['title']


class CourseInProgressSerializer(ModelSerializer):
    course = CourseSerializer()
    end_date = serializers.DateField(allow_null=True)

    class Meta:
        model = CourseInProgress
        fields = ['course', 'custom_title', 'start_date', 'end_date', 'is_finished']


class TaskInProgressSerializer(ModelSerializer):
    task = TaskSerializer()
    end_date = serializers.DateField(allow_null=True)

    class Meta:
        model = CourseInProgress
        fields = ['task', 'custom_title', 'start_date', 'end_date', 'is_finished', 'url']


class ProjectInProgressSerializer(ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = ProjectInProgress
        fields = ['project', 'custom_title', 'start_date', 'comments']


class ReportSerializer(ModelSerializer):
    intern = InternSerializer()
    courses = CourseInProgressSerializer(many=True, allow_null=True)
    tasks = TaskInProgressSerializer(many=True, allow_null=True)
    projects = ProjectInProgressSerializer(many=True, allow_null=True)

    def create(self, validated_data):

        pprint.pprint(validated_data)
        intern_params = validated_data.pop("intern")
        group_params = intern_params.pop("group")
        group = Group.objects.get_or_create(**group_params)[0]
        intern = Intern.objects.get_or_create(group=group, **intern_params)[0]

        courses_params = validated_data.pop("courses", None)
        courses_params = list(filter(lambda x: x is not None, courses_params))
        tasks_params = validated_data.pop("tasks", None)
        tasks_params = list(filter(lambda x: x is not None, tasks_params))
        projects_params = validated_data.pop("projects", None)
        projects_params = list(filter(lambda x: x is not None, projects_params))

        report = Report.objects.create(**validated_data, intern=intern)

        if courses_params:
            courses = [CourseInProgress.objects.create(
                course=Course.objects.get_or_create(title=course_in_progress.pop("course")['title'])[0], **course_in_progress,
                report=report) for course_in_progress in courses_params]

        if tasks_params:
            tasks = [TaskInProgress.objects.create(
                course=Task.objects.get_or_create(title=task_in_progress.pop("course")['title'])[0], **task_in_progress,
                report=report)
                for task_in_progress in tasks_params]

        if projects_params:
            projects = [TaskInProgress.objects.create(
                course=Task.objects.get_or_create(title=project_in_progress.pop("course")['title'])[0], **project_in_progress, report=report)
                for project_in_progress in projects_params]


        return report

    class Meta:
        model = Report
        fields = '__all__'

