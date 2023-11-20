from django.db import models


class Intern(models.Model):
    fname = models.CharField(verbose_name="Имя", max_length=200, null=False, blank=False)
    sname = models.CharField(verbose_name="Фамилия", max_length=200, null=False, blank=False)
    group = models.PositiveIntegerField("Номер группы", blank=False)
    telegram_id = models.IntegerField("ID Телеграм",)

    class Meta:
        verbose_name = "Стажёр"
        verbose_name_plural = "Стажёры"

    def __str__(self):
        return f"{self.sname} {self.fname}, гр. {self.group}"


class Report(models.Model):
    date = models.DateTimeField("Дата отправки отчёта")
    intern = models.ForeignKey(Intern, related_name="reports", on_delete=models.PROTECT)
