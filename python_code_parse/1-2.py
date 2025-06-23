import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
vacancies = pd.read_csv('vacancies_2024.csv')

# Преобразование даты публикации
vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], format='%Y-%m-%dT%H:%M:%S%z', errors='coerce', utc=True)

# Создание столбца года
vacancies['year'] = vacancies['published_at'].dt.year

# Подсчёт количества вакансий по годам
vacancy_count_by_year = vacancies.groupby('year').size().reset_index(name='vacancy_count')

# Сохранение таблицы в HTML
vacancy_count_by_year.to_html('student_works/vacancy_count_by_year.html', index=False)

# Построение графика
plt.figure(figsize=(24, 10))
plt.bar(vacancy_count_by_year['year'], vacancy_count_by_year['vacancy_count'], color='red', edgecolor='black')
plt.title('Динамика количества вакансий по годам', fontsize=14)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Количество вакансий', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(vacancy_count_by_year['year'])
plt.savefig('student_works/vacancy_count_trends.png')
plt.show()

print("Страница «Общая статистика» готова.")
