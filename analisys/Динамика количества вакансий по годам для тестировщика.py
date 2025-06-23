import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных
vacancies = pd.read_csv('vacancies_2024.csv')

# Преобразование даты в вакансии с учетом часовых поясов
vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], format='%Y-%m-%dT%H:%M:%S%z', errors='coerce', utc=True)

# Создание столбцов для года
if vacancies['published_at'].dtype == 'datetime64[ns, UTC]':
    vacancies['year'] = vacancies['published_at'].dt.year
else:
    print("Ошибка: столбец 'published_at' не имеет правильный формат datetime.")

# Фильтрация вакансий для профессии Тестировщик (QA-инженер)
keywords = ['qa', 'test', 'тест', 'quality assurance']
vacancies['is_test_job'] = vacancies['name'].str.lower().str.contains('|'.join(keywords))

# Отбор только вакансий для тестировщика
vacancies_test = vacancies[vacancies['is_test_job']]

print(f"Количество вакансий для Тестировщика: {vacancies_test.shape[0]}")

# Группировка данных по годам для подсчета вакансий тестировщика
vacancies_by_year_test = vacancies_test.groupby('year').size().reset_index(name='vacancy_count')

# Сохранение таблицы в HTML
vacancies_by_year_test.to_html('student_works/vacancies_by_year_test.html', index=False)

# Построение графика для динамики количества вакансий по годам для тестировщика
plt.figure(figsize=(24, 10))
plt.plot(vacancies_by_year_test['year'], vacancies_by_year_test['vacancy_count'], marker='o', color='#F4A460')
plt.title('Динамика количества вакансий для тестировщика по годам', fontsize=14)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Количество вакансий', fontsize=12)
plt.grid(True)

# Устанавливаем шаг в 1 год на оси X
plt.xticks(vacancies_by_year_test['year'])

# Сохраняем график
plt.savefig('student_works/vacancies_trends_test.png')
plt.show()

print("График и таблица для Тестировщика сохранены в папку student_works")
