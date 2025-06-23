import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных
vacancies = pd.read_csv('vacancies_2024.csv')
currencies = pd.read_csv('correct_result.csv')

# Преобразование даты в vacancies с учетом часовых поясов
vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], format='%Y-%m-%dT%H:%M:%S%z', errors='coerce', utc=True)

# Преобразование даты в currencies
currencies['date'] = pd.to_datetime(currencies['date'], format='%Y-%m')
currencies.set_index('date', inplace=True)

# Исключение вакансий с некорректной зарплатой
vacancies = vacancies[(vacancies['salary_from'] <= 10_000_000) & (vacancies['salary_to'] <= 10_000_000)]

# Вычисление средней зарплаты
vacancies['salary_avg'] = vacancies[['salary_from', 'salary_to']].mean(axis=1)

# Функция для получения курса валюты
def get_currency_rate(row, currency_data):
    if pd.isna(row['salary_currency']) or row['salary_currency'] == 'RUR':
        return 1  # Если валюта уже рубли
    date = row['published_at'].to_period('M').start_time  # Конвертируем период в timestamp
    currency_rate = currency_data.loc[date, row['salary_currency']] if row['salary_currency'] in currency_data.columns else np.nan
    return currency_rate

# Применение курса валют
vacancies['currency_rate'] = vacancies.apply(get_currency_rate, axis=1, currency_data=currencies)
vacancies['salary_rub'] = vacancies['salary_avg'] * vacancies['currency_rate']

# Фильтруем вакансии для профессии Тестировщик
keywords = ['qa', 'test', 'тест', 'quality assurance']
vacancies['is_qa'] = vacancies['name'].str.contains('|'.join(keywords), case=False, na=False)

qa_vacancies = vacancies[vacancies['is_qa']]

# Группировка данных по городам для вычисления среднего уровня зарплаты
salary_by_city = qa_vacancies.groupby('area_name')['salary_rub'].mean().reset_index()

# Округляем значения средней зарплаты до двух знаков после запятой
salary_by_city['salary_rub'] = salary_by_city['salary_rub'].round(2)

# Считаем долю вакансий по каждому городу
vacancies_count_by_city = qa_vacancies['area_name'].value_counts(normalize=True) * 100  # Доля в процентах

# Фильтруем только города, в которых доля вакансий > 1%
cities_with_more_than_1_percent = vacancies_count_by_city[vacancies_count_by_city > 1].index

# Оставляем только эти города
salary_by_city_filtered = salary_by_city[salary_by_city['area_name'].isin(cities_with_more_than_1_percent)]

# Сортировка по уровню зарплаты в порядке убывания
salary_by_city_sorted = salary_by_city_filtered.sort_values(by='salary_rub', ascending=False)

# Сохранение таблицы в HTML
salary_by_city_sorted.to_html('student_works/salary_by_city_filtered_qa.html', index=False)

# Построение горизонтального бар-чарта
plt.figure(figsize=(14, 8))
plt.barh(salary_by_city_sorted['area_name'], salary_by_city_sorted['salary_rub'], color='steelblue')
plt.title('Уровень зарплат по городам для тестировщиков (с долей вакансий > 1%)', fontsize=14)
plt.xlabel('Средняя зарплата (руб.)', fontsize=12)
plt.ylabel('Город', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Сохраняем график
plt.savefig('student_works/salary_by_city_filtered_qa_bar.png')
plt.show()

print("Горизонтальный бар-чарт и таблица уровня зарплат по городам для тестировщиков сохранены в папку student_works")
