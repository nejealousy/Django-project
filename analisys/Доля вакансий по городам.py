import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
vacancies = pd.read_csv('vacancies_2024.csv')

# Подсчет общего количества вакансий
total_vacancies = len(vacancies)

# Подсчет количества вакансий по городам
vacancies_count_by_city = vacancies['area_name'].value_counts()

# Рассчет доли вакансий по городам
vacancies_percentage_by_city = (vacancies_count_by_city / total_vacancies) * 100

# Фильтруем города с долей вакансий > 1%
cities_with_more_than_1_percent = vacancies_percentage_by_city[vacancies_percentage_by_city > 1]

# Округление доли вакансий до двух знаков после запятой
cities_with_more_than_1_percent = cities_with_more_than_1_percent.round(2)

# Сортировка по убыванию доли
cities_sorted = cities_with_more_than_1_percent.sort_values(ascending=False)

# Подготовка данных для сохранения таблицы
cities_table = pd.DataFrame({
    'City': cities_sorted.index,
    'Percentage': cities_sorted.values
})

# Сохранение таблицы в HTML
cities_table.to_html('student_works/vacancies_percentage_by_city.html', index=False)

# Построение графика
plt.figure(figsize=(24, 10))
plt.barh(cities_sorted.index, cities_sorted.values, color='steelblue')
plt.title('Доля вакансий по городам (с долей > 1%)', fontsize=16)
plt.xlabel('Доля вакансий (%)', fontsize=14)
plt.ylabel('Город', fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.gca().invert_yaxis()  # Инвертируем ось Y, чтобы топовые города были сверху

# Сохранение графика
plt.savefig('student_works/vacancies_percentage_by_city.png')
plt.show()

print("Таблица и график доли вакансий по городам сохранены в папку student_works")
