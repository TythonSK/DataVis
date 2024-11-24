from contextlib import nullcontext

import pandas as pd
from dotenv import load_dotenv
import os
import openai
import time

from pyexpat.errors import messages

# Načítanie API kľúča z .env súboru
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Funkcia na spracovanie otázky
def process_question(question):
    print("idem riesit otazku: ", question)
    # Inicializácia klienta OpenAI
    client = openai.Client(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that only answers questions about COVID-19 data from a dataset."},
            {"role": "user", "content": f"Question: {question}. Does this question refer to COVID-19 deaths?"}
        ]
    )

    gpt_response = response.choices[0].message.content

    if "áno" in gpt_response or "ano" in gpt_response or "Áno" in gpt_response or "Ano" in gpt_response\
            or "yes" in gpt_response or "Yes" in gpt_response:
        country_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract the country name from this question."},
                {"role": "user", "content": f"Question: {question}"}
            ]
        )
        country_name = country_response.choices[0].message.content

        continent_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "Your role is to provide information about countries and their continents."},
                {"role": "user", "content": f"Which continent is {country_name} located in?"}
            ]
        )

        continent = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract the continent name from this sentence."},
                {"role": "user", "content": f"Sentence: {continent_response.choices[0].message.content}"}
            ]
        )

        continent_name =  continent.choices[0].message.content
        print("continent name: ", continent_name)

        # country_name = "Albania"
        # return get_deaths_for_country(country_name)
        print("country respose: ", country_name)
        print(country_name, continent_name)
        return search_from_datasets(country_name, continent_name, question)
    else:
        return "I can't answer the question because it doesn't concern deaths from COVID-19."


# Príklad otázky
def search_from_datasets(country, continent, question):
    path = "C:/Users/Robik25/DataVis/backend/data"
    if continent == "Europe":
        path+= "/europe/time_series_covid19_deaths_global.csv"
    elif continent == "Asia":
        path+= "/asia/time_series_covid19_deaths_global.csv"
    elif continent == "Australia":
        path+= "/australia/time_series_covid19_deaths_global.csv"
    elif continent == "North America":
        path+= "/north_america/time_series_covid19_deaths_global.csv"
    elif continent == "South America":
        path+= "/south_america/time_series_covid19_deaths_global.csv"
    elif continent == "Africa":
        path+= "/africa/time_series_covid19_deaths_global.csv"
        

    print(path)



    # Načítanie datasetu
    dataset = pd.read_csv(path)
    if dataset is None:
        return f"Dataset pre kontinent {continent} nebol nájdený."
    print(path)

    country_data = dataset[dataset["Country/Region"] == country]
    total_deaths = country_data.iloc[:, 4:].sum(axis=0).sum()
    print(f"Total deaths: {total_deaths}")

    prompt = f"""
    Question: {question}
    Country: {country}
    Total Deaths: {total_deaths}
    You must provide a simple answer to the question asked based on this available data.
    """
    client = openai.Client(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant who answers a question."},
            {"role": "user", "content": prompt}
        ]
    )

    # Vrátenie odpovede
    answer = response.choices[0].message.content
    return answer


if __name__ == "__main__":
    question = "How many people died from covid 19 in China?"
    result = process_question(question)
    print(result)

