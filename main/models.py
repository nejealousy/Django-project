from django.db import models

class GeneralStatistics(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок страницы")
    description = models.TextField(blank=True, verbose_name="Описание страницы")

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"

    def __str__(self):
        return self.title


class StatisticsSection(models.Model):
    general_statistics = models.ForeignKey(
        GeneralStatistics,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name="Общая статистика"
    )
    title = models.CharField(max_length=255, verbose_name="Название раздела")
    table_html = models.TextField(verbose_name="HTML таблица")
    graph = models.ImageField(upload_to='statistics/graphs/', verbose_name="График")

    class Meta:
        verbose_name = "Раздел статистики"
        verbose_name_plural = "Разделы статистики"

    def __str__(self):
        return self.title
