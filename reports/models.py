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

    class Meta:
        verbose_name = "Стажёр"
        verbose_name_plural = "Стажёры"

    def __str__(self):
        return f"{self.name}, {self.group}"


class Report(models.Model):
    date = models.DateTimeField("Дата отправки отчёта")
    intern = models.ForeignKey(Intern, related_name="reports", on_delete=models.PROTECT)
    raw_report_data = models.JSONField(verbose_name="Отчёт")

    class Meta:
        verbose_name = "Отчёт"
        verbose_name_plural = "Отчёты"

    def __str__(self):
        return f"Отчёт #{self.id} {self.date}, от {self.intern}"
