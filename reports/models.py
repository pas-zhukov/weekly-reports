from django.db import models


class Group(models.Model):
    number = models.PositiveIntegerField("Номер группы", blank=False)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return f"гр. {self.number}"


class Intern(models.Model):
    name = models.CharField(verbose_name="ФИО", max_length=200, null=False, blank=False)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name="interns")
    telegram_id = models.IntegerField("ID Телеграм",)

    is_active = models.BooleanField("Активен как стажёр", default=True)

    class Meta:
        verbose_name = "Стажёр"
        verbose_name_plural = "Стажёры"

    def __str__(self):
        return f"{self.name}, {self.group}"


class Course(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"{self.title}"


class Task(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        verbose_name = "Практическая задача"
        verbose_name_plural = "Практические задачи"

    def __str__(self):
        return f"{self.title}"


class InProgress(models.Model):
    custom_title = models.CharField(max_length=500, blank=True)
    start_date = models.DateField("Дата начала", null=False, blank=False)
    end_date = models.DateField("Дата окончания", null=True, blank=True)
    is_finished = models.BooleanField("Работа завершена", default=False)


class CourseInProgress(InProgress):
    course = models.ForeignKey(Course, related_name="in_progress", on_delete=models.PROTECT)
    report = models.ForeignKey("Report", related_name="courses", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Курс в работе"
        verbose_name_plural = "Курсы в работе"

    def __str__(self):
        return f"{self.course.title} - в работе, id#{self.id}"


class TaskInProgress(InProgress):
    task = models.ForeignKey(Task, related_name="in_progress", on_delete=models.PROTECT)
    report = models.ForeignKey("Report", related_name="tasks", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Практическая задача в работе"
        verbose_name_plural = "Практические задачи в работе"

    def __str__(self):
        return f"{self.task.title} - в работе, id#{self.id}"


class Report(models.Model):
    date = models.DateTimeField("Дата отправки отчёта")
    intern = models.ForeignKey(Intern, related_name="reports", on_delete=models.PROTECT)

    department = models.CharField("Целевой отдел", max_length=20)
    current_state = models.CharField("Статус", max_length=50)
    courses_count = models.PositiveIntegerField("Кол-во курсов в работе", null=True, blank=True)
    other_courses = models.TextField("Информация об остальных курсах", blank=True)
    tasks_count = models.PositiveIntegerField("Кол-во задач в работе", null=True, blank=True)

    project_name = ...
    project_start_date = ...
    project_comments = ...

    time_spent = ...

    progress_comment = ...
    next_week_url = ...
    difficulties = ...
    additional_comment = ...

    class Meta:
        verbose_name = "Отчёт"
        verbose_name_plural = "Отчёты"

    def __str__(self):
        return f"Отчёт #{self.id} {self.date}, от {self.intern}"
