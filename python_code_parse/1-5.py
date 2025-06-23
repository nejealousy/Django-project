import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
vacancies = pd.read_csv('../../../vacancies_2024.csv')

# Преобразование даты
vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], format='%Y-%m-%dT%H:%M:%S%z', errors='coerce', utc=True)

# Создание столбца года
vacancies['year'] = vacancies['published_at'].dt.year

# Исключение строк с пустыми навыками
vacancies = vacancies.dropna(subset=['key_skills'])

# Разделение навыков на отдельные строки
skills = vacancies[['year', 'key_skills']].copy()
skills['key_skills'] = skills['key_skills'].str.split('\n')  # Разделитель '\n'
skills = skills.explode('key_skills')  # Разделяем навыки на отдельные строки
skills['key_skills'] = skills['key_skills'].str.strip()  # Убираем лишние пробелы

# Подсчёт частоты навыков по годам
top_skills_by_year = (
    skills.groupby(['year', 'key_skills'])
    .size()
    .reset_index(name='count')
    .sort_values(['year', 'count'], ascending=[True, False])
)

# Отбор топ-20 навыков для каждого года
top_20_skills_by_year = (
    top_skills_by_year.groupby('year')
    .head(20)
    .reset_index(drop=True)
)

# Создание HTML таблицы по годам
html_content = '<table border="1" style="border-collapse:collapse; text-align:left;">'
html_content += '<thead><tr><th>Год</th><th>Навык</th><th>Частота</th></tr></thead><tbody>'

current_year = None
rowspan_count = 0

for _, row in top_20_skills_by_year.iterrows():
    if row['year'] != current_year:
        if rowspan_count > 0:  # Завершаем предыдущую группу rowspan
            html_content = html_content.replace(f'ROWSPAN_PLACEHOLDER_{current_year}', str(rowspan_count))
        current_year = row['year']
        rowspan_count = 0
        html_content += f'<tr><td rowspan="ROWSPAN_PLACEHOLDER_{current_year}">{current_year}</td><td>{row["key_skills"]}</td><td>{row["count"]}</td></tr>'
    else:
        html_content += f'<tr><td>{row["key_skills"]}</td><td>{row["count"]}</td></tr>'
    rowspan_count += 1

# Завершаем последнюю группу rowspan
if rowspan_count > 0:
    html_content = html_content.replace(f'ROWSPAN_PLACEHOLDER_{current_year}', str(rowspan_count))

html_content += '</tbody></table>'

# Сохранение в файл
with open('student_works/top_20_skills_by_year.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML таблица с объединёнными ячейками создана.")

# Построение графика для выбранного года
year_to_plot = 2024
skills_2024 = top_20_skills_by_year[top_20_skills_by_year['year'] == year_to_plot]

plt.figure(figsize=(24, 10))
plt.barh(skills_2024['key_skills'], skills_2024['count'], color='blue')
plt.title(f'Топ-20 навыков в {year_to_plot} году', fontsize=14)
plt.xlabel('Частота упоминания', fontsize=12)
plt.ylabel('Навыки', fontsize=12)
plt.gca().invert_yaxis()  # Перевернуть ось Y для лучшей читаемости
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Сохранение графика
plt.savefig(f'student_works/top_20_skills_{year_to_plot}.png')
plt.show()

#
# # Подсчёт топ-20 навыков за всё время
# top_skills_all_time = (
#     skills.groupby('key_skills')
#     .size()
#     .reset_index(name='count')
#     .sort_values('count', ascending=False)
#     .head(20)
# )
#
# # Создание HTML таблицы для топ-20 навыков за всё время
# html_content_all_time = '<table border="1" style="border-collapse:collapse; text-align:left;">'
# html_content_all_time += '<thead><tr><th>Навык</th><th>Частота</th></tr></thead><tbody>'
#
# for _, row in top_skills_all_time.iterrows():
#     html_content_all_time += f'<tr><td>{row["key_skills"]}</td><td>{row["count"]}</td></tr>'
#
# html_content_all_time += '</tbody></table>'
#
# # Сохранение в файл
# with open('student_works/top_20_skills_all_time.html', 'w', encoding='utf-8') as f:
#     f.write(html_content_all_time)
#
# print("HTML таблица топ-20 навыков за всё время создана.")
#
# # Построение графика для топ-20 навыков за всё время
# plt.figure(figsize=(24, 10))
# plt.barh(top_skills_all_time['key_skills'], top_skills_all_time['count'], color='lightcoral')
# plt.title('Топ-20 навыков за всё время', fontsize=14)
# plt.xlabel('Частота упоминания', fontsize=12)
# plt.ylabel('Навыки', fontsize=12)
# plt.gca().invert_yaxis()  # Перевернуть ось Y для лучшей читаемости
# plt.grid(axis='x', linestyle='--', alpha=0.7)
#
# # Сохранение графика
# plt.savefig('student_works/top_20_skills_all_time.png')
# plt.show()
