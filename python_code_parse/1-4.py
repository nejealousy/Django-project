import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
vacancies = pd.read_csv('vacancies_2024.csv')

# Подсчёт общего количества вакансий
total_vacancies = len(vacancies)

# Подсчёт количества вакансий по городам
vacancy_counts = vacancies['area_name'].value_counts()

# Вычисление доли вакансий по городам
vacancy_shares = (vacancy_counts / total_vacancies * 100).reset_index()
vacancy_shares.columns = ['area_name', 'vacancy_share']

# Сортировка по убыванию доли
vacancy_shares = vacancy_shares.sort_values(by='vacancy_share', ascending=False)

# Оставляем только топ-10 городов
top_cities = vacancy_shares.head(10).copy()

# Округление долей до двух знаков после запятой
top_cities['vacancy_share'] = top_cities['vacancy_share'].round(2)

# Сохранение таблицы в HTML
top_cities.to_html('student_works/vacancy_shares_by_city.html', index=False)

# Построение круговой диаграммы
plt.figure(figsize=(24, 10))
plt.pie(
    top_cities['vacancy_share'],
    labels=top_cities['area_name'].str.replace(' ', '\n'),
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Paired.colors
)
plt.title('Доля вакансий по городам (в %)', fontsize=14)
plt.savefig('student_works/vacancy_shares_by_city.png')
plt.show()

print("Анализ доли вакансий по городам завершён.")

