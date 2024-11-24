import pandas as pd
from dotenv import load_dotenv
import os
import openai

# Načítanie API kľúča z .env súboru
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Načítanie datasetu
data = pd.read_csv("data/europe/time_series_covid19_deaths_global.csv")


# Preprocessing dát: zgrupujeme podľa krajín
def preprocess_data(data):
    if "Country/Region" in data.columns:
        country_col = "Country/Region"
    elif "Region" in data.columns:
        country_col = "Region"
    else:
        raise ValueError("Dataset neobsahuje stĺpec s názvom krajiny.")

    # Skupina dát podľa krajín a spočítanie celkových úmrtí
    grouped_data = data.groupby(country_col).sum()
    return grouped_data


grouped_data = preprocess_data(data)


# Funkcia na získanie úmrtí pre danú krajinu
def get_deaths_for_country(country_name):
    if country_name not in grouped_data.index:
        return f"Dáta pre krajinu {country_name} nie sú k dispozícii."
    total_deaths = grouped_data.loc[country_name].sum()
    return f"Celkový počet úmrtí v krajine {country_name} je {int(total_deaths)}."

# Funkcia na spracovanie otázky
def process_question(question):
    print("idem riesit otazku: ", question)
    # Inicializácia klienta OpenAI
    client = openai.Client(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that only answers questions about COVID-19 data from a dataset."},
            # {"role": "user", "content": f"Otázka: {question}. Týka sa táto otázka COVID-19 úmrtí v konkrétnej krajine?"}
        ]
    )

    gpt_response = response.choices[0].message.content
    print("toto je response: ", gpt_response)

    if "áno" in gpt_response or "ano" in gpt_response or "Áno" in gpt_response or "Ano" in gpt_response\
            or "yes" in gpt_response or "Yes" in gpt_response:
        country_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Si AI asistent. Extrahuj názov krajiny z nasledujúcej otázky a prelož ho do angličtiny."},
                {"role": "user", "content": f"Otázka: {question}"}
            ]
        )
        country_name = country_response.choices[0].message.content
        #country_name = "Albania"
        return get_deaths_for_country(country_name)
    else:
        return "Neviem odpovedať na otázku, pretože sa netýka úmrtí na COVID-19."


# Príklad otázky
if __name__ == "__main__":
    question = "How much people dead on covid-19 in Slovakia?"
    print(process_question(question))
