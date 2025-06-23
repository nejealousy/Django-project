import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import os

# Убедимся, что папка student_works существует
output_dir = 'student_works'
os.makedirs(output_dir, exist_ok=True)

# Загрузка данных
vacancies = pd.read_csv('vacancies_2024.csv')

# Преобразование даты в формат datetime
vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], errors='coerce', utc=True)

# Извлечение года из даты
vacancies['year'] = vacancies['published_at'].dt.year

# Установка диапазона годов
start_year = 2015
end_year = 2024

# Обработка по годам
for year in range(start_year, end_year + 1):
    # Фильтрация данных для указанного года
    yearly_vacancies = vacancies[vacancies['year'] == year]

    if yearly_vacancies.empty:
        print(f"Нет данных для года {year}")
        continue

    # Обработка навыков
    yearly_vacancies['key_skills'] = yearly_vacancies['key_skills'].fillna('')  # Заменяем NaN на пустую строку
    skills = Counter()
    for skills_list in yearly_vacancies['key_skills']:
        skills.update(skill.strip() for skill in skills_list.split('\n') if skill.strip())  # Считаем навыки

    # Топ-20 навыков
    top_skills = skills.most_common(20)

    # Создаем DataFrame для таблицы
    table_data = pd.DataFrame(top_skills, columns=['Skill', 'Frequency'])

    # Генерация HTML таблицы с объединенной ячейкой для года
    html_output = f"""
    <table border="1" style="border-collapse: collapse; width: 100%; text-align: center; font-size: 14px;">
        <thead>
            <tr>
                <th style="width: 15%; text-align: center;">Год</th>
                <th style="width: 50%; text-align: center;">Навык</th>
                <th style="width: 35%; text-align: center;">Частота</th>
            </tr>
        </thead>
        <tbody>
    """

    # Добавляем объединенную ячейку для года
    html_output += f"""
            <tr>
                <td rowspan="{len(top_skills)}" style="vertical-align: middle; text-align: center; font-weight: bold; font-size: 18px;">
                    {year}
                </td>
    """

    # Добавляем строки с навыками
    for i, row in table_data.iterrows():
        skill = row['Skill']
        frequency = row['Frequency']
        if i > 0:  # Первая строка уже начата выше
            html_output += "<tr>"
        html_output += f"""
                <td>{skill}</td>
                <td>{frequency}</td>
            </tr>
        """

    html_output += """
        </tbody>
    </table>
    """

    # Сохраняем HTML файл
    html_path = os.path.join(output_dir, f'top_skills_{year}.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"Таблица сохранена в файл: {html_path}")

    # Построение графика
    plt.figure(figsize=(12, 6))
    skills_names, frequencies = zip(*top_skills)
    plt.barh(skills_names, frequencies, color='steelblue')
    plt.xlabel('Частота упоминаний', fontsize=12)
    plt.ylabel('Навыки', fontsize=12)
    plt.title(f'Топ-20 навыков за {year} год', fontsize=14)
    plt.gca().invert_yaxis()  # Инвертируем ось Y, чтобы самый популярный навык был сверху
    plt.tight_layout()

    # Сохраняем график
    graph_path = os.path.join(output_dir, f'top_skills_{year}.png')
    plt.savefig(graph_path)
    plt.close()

    print(f"График сохранен в файл: {graph_path}")

print("Обработка завершена.")
