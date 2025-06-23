from django.shortcuts import render, get_object_or_404
from .models import GeneralStatistics
from datetime import datetime, timedelta
import requests

def index(request):
    return render(request, 'main/index.html')

# Последние вакансии QA
def get_QA_vacancies():
    date_to = datetime.now()
    date_from = date_to - timedelta(days=1)

    url = "https://api.hh.ru/vacancies"
    params = {
        "text": '("qa" OR "тест" OR "test" OR "quality assurance")',
        "search_field": "name",  # Ищем по названию вакансии
        "date_from": date_from.strftime("%Y-%m-%dT%H:%M:%S"),
        "date_to": date_to.strftime("%Y-%m-%dT%H:%M:%S"),
        "per_page": 10,
        "page": 0,
    }

    headers = {"User-Agent": "QAVacancyFetcher/1.0"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        vacancies = response.json().get("items", [])
        detailed_vacancies = []

        for vacancy in vacancies:
            vacancy_id = vacancy["id"]
            details_url = f"{url}/{vacancy_id}"
            details_response = requests.get(details_url, headers=headers)
            details_response.raise_for_status()
            vacancy_details = details_response.json()

            detailed_vacancies.append({
                "name": vacancy_details.get("name"),
                "description": vacancy_details.get("description", "Описание не указано"),
                "skills": ", ".join(skill["name"] for skill in vacancy_details.get("key_skills", [])),
                "company": vacancy_details.get("employer", {}).get("name", "Компания не указана"),
                "salary": format_salary(vacancy_details.get("salary")),
                "region": vacancy_details.get("area", {}).get("name", "Регион не указан"),
                "published_at": format_date(vacancy_details.get("published_at")),
            })

        return detailed_vacancies

    except requests.RequestException as e:
        print(f"Ошибка при запросе к API HH: {e}")
        return None


def format_salary(salary):
    if not salary:
        return "Не указана"
    if salary["from"] and salary["to"]:
        return f"{salary['from']}–{salary['to']} {salary['currency']}"
    elif salary["from"]:
        return f"От {salary['from']} {salary['currency']}"
    elif salary["to"]:
        return f"До {salary['to']} {salary['currency']}"
    return "Не указана"


def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
        return date_obj.strftime("%d.%m.%Y, %H:%M")
    except ValueError:
        return "Дата не распознана"


def latest_vacancies(request):
    vacancies = get_QA_vacancies()
    return render(request, "main/latest_vacancies.html", {"vacancies": vacancies})