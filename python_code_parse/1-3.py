import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных
vacancies = pd.read_csv('vacancies_2024.csv')
currencies = pd.read_csv('currency.csv')

# Преобразование даты в vacancies с учетом часовых поясов
vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], format='%Y-%m-%dT%H:%M:%S%z', errors='coerce', utc=True)

# Создание столбцов для года и месяца
if vacancies['published_at'].dtype == 'datetime64[ns, UTC]':
    vacancies['month'] = vacancies['published_at'].dt.to_period('M')
else:
    print("Ошибка: столбец 'published_at' не имеет правильный формат datetime.")

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
    date = row['month'].to_timestamp()  # Конвертируем период в timestamp
    currency_rate = currency_data.loc[date, row['salary_currency']] if row['salary_currency'] in currency_data.columns else np.nan
    return currency_rate

# Применение курса валют
vacancies['currency_rate'] = vacancies.apply(get_currency_rate, axis=1, currency_data=currencies)
vacancies['salary_rub'] = vacancies['salary_avg'] * vacancies['currency_rate']

# Подсчёт количества вакансий по городам
vacancy_counts = vacancies['area_name'].value_counts()

# Фильтрация городов, где количество вакансий > 1% от общего числа вакансий
total_vacancies = len(vacancies)
valid_cities = vacancy_counts[vacancy_counts > (total_vacancies * 0.01)].index

# Фильтрация вакансий по городам
vacancies = vacancies[vacancies['area_name'].isin(valid_cities)]

# Группировка данных по городам
salary_by_city = (
    vacancies.groupby('area_name')['salary_rub']
    .mean()
    .reset_index()
    .rename(columns={'salary_rub': 'average_salary_rub'})
)

# Сортировка по убыванию средней зарплаты
salary_by_city = salary_by_city.sort_values(by='average_salary_rub', ascending=False)

# Округление средней зарплаты до двух знаков
salary_by_city['average_salary_rub'] = salary_by_city['average_salary_rub'].round(2)

# Сохранение таблицы в HTML
salary_by_city.to_html('student_works/salary_by_city.html', index=False)

# Построение графика
plt.figure(figsize=(24, 10))
plt.barh(salary_by_city['area_name'], salary_by_city['average_salary_rub'], color='red', edgecolor='black')
plt.title('Уровень зарплат по городам (в рублях)', fontsize=14)
plt.xlabel('Средняя зарплата (руб.)', fontsize=12)
plt.ylabel('Город', fontsize=12)
plt.gca().invert_yaxis()  # Переворачиваем ось Y для лучшей читаемости
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.savefig('student_works/salary_by_city.png')
plt.show()

print("Анализ уровня зарплат по городам завершён.")
