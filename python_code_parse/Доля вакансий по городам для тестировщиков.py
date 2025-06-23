import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
vacancies = pd.read_csv('vacancies_2024.csv')

# Фильтруем вакансии для профессии Тестировщик
keywords = ['qa', 'test', 'тест', 'quality assurance']
vacancies['is_qa'] = vacancies['name'].str.contains('|'.join(keywords), case=False, na=False)

qa_vacancies = vacancies[vacancies['is_qa']]

# Подсчет общего количества вакансий для тестировщиков
total_qa_vacancies = len(qa_vacancies)

# Подсчет количества вакансий по городам для тестировщиков
qa_vacancies_count_by_city = qa_vacancies['area_name'].value_counts()

# Рассчет доли вакансий по городам для тестировщиков
qa_vacancies_percentage_by_city = (qa_vacancies_count_by_city / total_qa_vacancies) * 100

# Округление долей до двух знаков после запятой
qa_vacancies_percentage_by_city = qa_vacancies_percentage_by_city.round(2)

# Фильтруем города с долей вакансий > 1%
qa_cities_with_more_than_1_percent = qa_vacancies_percentage_by_city[qa_vacancies_percentage_by_city > 1]

# Сортировка по убыванию доли
qa_cities_sorted = qa_cities_with_more_than_1_percent.sort_values(ascending=False)

# Подготовка данных для сохранения таблицы
qa_cities_table = pd.DataFrame({
    'City': qa_cities_sorted.index,
    'Percentage': qa_cities_sorted.values
})

# Сохранение таблицы в HTML
qa_cities_table.to_html('student_works/qa_vacancies_percentage_by_city.html', index=False)

# Построение столбчатого графика
plt.figure(figsize=(12, 8))
plt.bar(qa_cities_sorted.index, qa_cities_sorted.values, color='steelblue', width=0.6)

# Добавление подписей и стиля
plt.title('Доля вакансий по городам для тестировщиков (с долей > 1%)', fontsize=16)
plt.xlabel('Города', fontsize=12)
plt.ylabel('Доля вакансий (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Сохранение графика
plt.tight_layout()
plt.savefig('student_works/qa_vacancies_percentage_by_city_bar.png')
plt.show()

print("Таблица и столбчатый график доли вакансий по городам для тестировщиков сохранены в папку student_works.")
