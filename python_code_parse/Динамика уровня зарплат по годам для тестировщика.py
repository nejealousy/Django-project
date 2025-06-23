import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных
vacancies = pd.read_csv('vacancies_2024.csv', low_memory=False)
currencies = pd.read_csv('correct_result.csv')

# Преобразование даты в vacancies с учетом часовых поясов
vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], format='%Y-%m-%dT%H:%M:%S%z', errors='coerce', utc=True)

# Отладка: проверим тип данных в столбце 'published_at' и наличие NaT
print("Тип данных в 'published_at':", vacancies['published_at'].dtype)
print("Количество NaT в 'published_at':", vacancies['published_at'].isna().sum())

# Выведем несколько строк для проверки
print(vacancies['published_at'].head())

# Создание столбцов для года и месяца, если преобразование прошло успешно
if vacancies['published_at'].dtype == 'datetime64[ns, UTC]':
    vacancies['year'] = vacancies['published_at'].dt.year
    vacancies['month'] = vacancies['published_at'].dt.to_period('M')
else:
    print("Ошибка: столбец 'published_at' не имеет правильный формат datetime.")

# Преобразование даты в currencies
currencies['date'] = pd.to_datetime(currencies['date'], format='%Y-%m')
currencies.set_index('date', inplace=True)

print("первая часть готова")

# Исключение вакансий с некорректной зарплатой
vacancies = vacancies[(vacancies['salary_from'] <= 10_000_000) & (vacancies['salary_to'] <= 10_000_000)]

# Фильтрация вакансий для профессии Тестировщик (QA-инженер)
keywords = ['qa', 'test', 'тест', 'quality assurance']
vacancies['is_test_job'] = vacancies['name'].str.lower().str.contains('|'.join(keywords))

# Отбор только тех вакансий, которые относятся к профессии "Тестировщик"
vacancies_test = vacancies[vacancies['is_test_job']]

print(f"Количество вакансий для Тестировщика: {vacancies_test.shape[0]}")

# Вычисление средней зарплаты
vacancies_test['salary_avg'] = vacancies_test[['salary_from', 'salary_to']].mean(axis=1)

print("вторая часть готова")

# Функция для получения курса валюты
def get_currency_rate(row, currency_data):
    if pd.isna(row['salary_currency']) or row['salary_currency'] == 'RUR':
        return 1  # Если валюта уже рубли
    date = row['month'].to_timestamp()  # Конвертируем период в timestamp
    currency_rate = currency_data.loc[date, row['salary_currency']] if row['salary_currency'] in currency_data.columns else np.nan
    return currency_rate

# Применение курса валют
vacancies_test['currency_rate'] = vacancies_test.apply(get_currency_rate, axis=1, currency_data=currencies)
vacancies_test['salary_rub'] = vacancies_test['salary_avg'] * vacancies_test['currency_rate']

print("третья часть готова")

# Группировка данных
salary_by_year_test = vacancies_test.groupby('year')['salary_rub'].mean().reset_index()
salary_by_year_test.rename(columns={'salary_rub': 'average_salary_rub'}, inplace=True)

# Округление средней зарплаты до двух знаков после запятой
salary_by_year_test['average_salary_rub'] = salary_by_year_test['average_salary_rub'].round(2)

print("четвертая часть готова")

# Сохранение таблицы в HTML с округленными значениями
salary_by_year_test.to_html('student_works/qa_salary_by_year.html', index=False)

print("пятая часть готова")

# Построение графика с шагом в 1 год на оси X
plt.figure(figsize=(24, 10))
plt.plot(salary_by_year_test['year'], salary_by_year_test['average_salary_rub'], marker='o', color='#F4A460')
plt.title('Динамика уровня зарплат для тестировщика по годам (в рублях)', fontsize=14)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Средняя зарплата (руб.)', fontsize=12)
plt.grid(True)

# Устанавливаем шаг в 1 год на оси X
plt.xticks(salary_by_year_test['year'])

# Сохранение графика
plt.savefig('student_works/qa_salary_trends.png')
plt.show()

print("код выполнен")
