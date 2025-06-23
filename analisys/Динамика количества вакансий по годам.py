import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных
vacancies = pd.read_csv('vacancies_2024.csv')
currencies = pd.read_csv('correct_result.csv')

# Преобразование даты в vacancies с учетом часовых поясов
vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], format='%Y-%m-%dT%H:%M:%S%z', errors='coerce', utc=True)

# Создание столбцов для года и месяца
if vacancies['published_at'].dtype == 'datetime64[ns, UTC]':
    vacancies['year'] = vacancies['published_at'].dt.year
else:
    print("Ошибка: столбец 'published_at' не имеет правильный формат datetime.")

# Группировка данных по годам для подсчета вакансий
vacancies_by_year = vacancies.groupby('year').size().reset_index(name='vacancy_count')

# Сохранение таблицы в HTML
vacancies_by_year.to_html('student_works/vacancies_by_year.html', index=False)

# Построение графика для динамики количества вакансий по годам
plt.figure(figsize=(24, 10))
plt.plot(vacancies_by_year['year'], vacancies_by_year['vacancy_count'], marker='o', color='#F4A460')
plt.title('Динамика количества вакансий по годам', fontsize=14)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Количество вакансий', fontsize=12)
plt.grid(True)

# Устанавливаем шаг в 1 год на оси X
plt.xticks(vacancies_by_year['year'])

# Сохраняем график
plt.savefig('student_works/vacancies_trends.png')
plt.show()

print("График и таблица сохранены в папку student_works")

