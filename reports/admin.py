from django.contrib import admin

from .models import Group, Intern
from .models import Course, Task, Project
from .models import CourseInProgress, TaskInProgress, ProjectInProgress
from .models import Report


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    ...


@admin.register(Intern)
class InternAdmin(admin.ModelAdmin):
    ...


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    ...


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    ...


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    ...


@admin.register(CourseInProgress)
class CourseInProgressAdmin(admin.ModelAdmin):
    ...


@admin.register(TaskInProgress)
class TaskInProgressAdmin(admin.ModelAdmin):
    ...


@admin.register(ProjectInProgress)
class ProjectInProgressAdmin(admin.ModelAdmin):
    ...


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    ...