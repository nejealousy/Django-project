from django.contrib import admin
from .models import GeneralStatistics, StatisticsSection

class StatisticsSectionInline(admin.TabularInline):
    model = StatisticsSection
    extra = 1  # Количество пустых строк для добавления новых разделов


@admin.register(GeneralStatistics)
class GeneralStatisticsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [StatisticsSectionInline]
