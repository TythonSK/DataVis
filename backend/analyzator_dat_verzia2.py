# import pandas as pd
# from dotenv import load_dotenv
# import os
# import openai
#
#
# class Analyzator_datasetu():
#     def __init__(self, question):
#         # Načítanie API kľúča z .env súboru
#         load_dotenv()
#         self.api_key = os.getenv("OPENAI_API_KEY")
#         if not self.api_key:
#             raise ValueError("API key is not found in the .env file.")
#         # openai.api_key = self.api_key
#         # question = "How many people died from covid 19 in China?"
#         self.question = question
#         # Načítanie API kľúča z .env súboru
#         load_dotenv()
#         api_key = os.getenv("OPENAI_API_KEY")
#         result = self.process_question(question, api_key)
#         print(result)
#
#
#
#     def calculate_deaths_in_intervals(country_data, interval_days):
#         # Vyber stĺpce s dátami (od piateho stĺpca, keďže predchádzajúce stĺpce sú pre metadáta)
#         death_data = country_data.iloc[:, 4:]
#
#         # Spočítanie úmrtí po daných intervaloch
#         deaths_by_intervals = []
#         num_columns = death_data.shape[1]
#
#         for start in range(0, num_columns, interval_days):
#             end = min(start + interval_days, num_columns)
#             interval_sum = death_data.iloc[:, start:end].sum(axis=1).values[0]
#
#             # Konvertovanie na int a pridanie do zoznamu
#             deaths_by_intervals.append(int(interval_sum))
#
#         return deaths_by_intervals
#
#
#     # Funkcia na spracovanie otázky
#     def process_question(question, api_key):
#         print("Idem riešiť otázku: ", question)
#
#         client = openai.Client(api_key=api_key)
#
#         # Inicializácia klienta OpenAI
#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system",
#                  "content": "You are an AI assistant that only answers questions about COVID-19 data from a dataset."},
#                 {"role": "user", "content": f"Question: {question}. Does this question refer to COVID-19 deaths?"}
#             ]
#         )
#         gpt_response = response.choices[0].message.content
#         print(gpt_response)
#
#         if "áno" in gpt_response.lower() or "yes" in gpt_response.lower() or "Yes" in gpt_response.lower() or "Áno" in gpt_response.lower():
#             # Extrahovanie názvu krajiny
#             country_response = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system", "content": "Extract the country name from this question."},
#                     {"role": "user", "content": f"Question: {question}"}
#                 ]
#             )
#             country_name = country_response.choices[0].message.content
#             print(country_name)
#
#             # Extrahovanie intervalu z otázky
#             interval_days = 30  # predvolený interval 30 dní
#             interval_response = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system", "content": "Extract the interval in days from this question, if mentioned."},
#                     {"role": "user", "content": f"Question: {question}"}
#                 ]
#             )
#             try:
#                 interval_days = int(interval_response.choices[0].message.content.strip())
#                 print(f"Použitý interval: {interval_days} dní.")
#             except ValueError:
#                 print(f"Nepodarilo sa extrahovať interval, používa sa predvolený interval {interval_days} dní.")
#
#             # Extrahovanie kontinentu
#             continent_response = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system",
#                      "content": "Your role is to provide information about countries and their continents."},
#                     {"role": "user", "content": f"Which continent is {country_name} located in?"}
#                 ]
#             )
#
#             continent = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[
#                     {"role": "system", "content": "Extract the continent name from this sentence."},
#                     {"role": "user", "content": f"Sentence: {continent_response.choices[0].message.content}"}
#                 ]
#             )
#
#             continent_name = continent.choices[0].message.content
#             print("Continent name: ", continent_name)
#
#             return question.search_from_datasets(country_name, continent_name, interval_days, question)
#         else:
#             return "I can't answer the question because it doesn't concern deaths from COVID-19."
#
#
#     # Funkcia na vyhľadávanie v datasete
#     def search_from_datasets(country, continent, interval_days, question):
#         path = "data"
#         if continent == "Europe":
#             path+= "/europe/time_series_covid19_deaths_global.csv"
#         elif continent == "Asia":
#             path+= "/asia/time_series_covid19_deaths_global.csv"
#         elif continent == "Australia":
#             path+= "/australia/time_series_covid19_deaths_global.csv"
#         elif continent == "North America":
#             path+= "/north_america/time_series_covid19_deaths_global.csv"
#         elif continent == "South America":
#             path+= "/south_america/time_series_covid19_deaths_global.csv"
#         elif continent == "Africa":
#             path+= "/africa/time_series_covid19_deaths_global.csv"
#
#         # Načítanie datasetu
#         print(path)
#         dataset = pd.read_csv(path)
#         if dataset is None:
#             return f"Dataset pre kontinent {continent} nebol nájdený."
#
#         # Filtrovanie údajov pre konkrétnu krajinu
#         if "Country/Region" not in dataset.columns:
#             return f"Expected column 'Country/Region' was not found in the dataset."
#
#         country_data = dataset[dataset["Country/Region"] == country]
#         if country_data.empty:
#             return f"No data found for country {country} in the dataset."
#
#         # Rozdelenie údajov podľa zadaného intervalu
#         deaths_by_intervals = country.calculate_deaths_in_intervals(country_data, interval_days)
#         print(f"Deaths in {interval_days}-day intervals:")
#         print(deaths_by_intervals)
#
#         # Zápis do CSV súboru (iba číselné hodnoty v jednom riadku)
#         output_path = "deaths_by_intervals.csv"
#         with open(output_path, 'w') as f:
#             f.write(",".join(map(str, deaths_by_intervals)))
#
#         print(f"Výsledky boli úspešne uložené do súboru: {output_path}")
#
#         # Vrátenie odpovede ako pole číselných hodnôt
#         return deaths_by_intervals
#
#
#     # if __name__ == "__main__":
#     #     question = "How many people died from covid 19 in Slovakia every 100 days?"
#     #     result = process_question(question)
#     #     print(result)



import pandas as pd
from dotenv import load_dotenv
import os
import openai

# Načítanie API kľúča z .env súboru
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def calculate_deaths_in_intervals(country_data, interval_days):
    # Vyber stĺpce s dátami (od piateho stĺpca, keďže predchádzajúce stĺpce sú pre metadáta)
    death_data = country_data.iloc[:, 4:]

    # Spočítanie úmrtí po daných intervaloch
    deaths_by_intervals = []
    num_columns = death_data.shape[1]

    for start in range(0, num_columns, interval_days):
        end = min(start + interval_days, num_columns)
        interval_sum = death_data.iloc[:, start:end].sum(axis=1).values[0]

        # Konvertovanie na int a pridanie do zoznamu
        deaths_by_intervals.append(int(interval_sum))

    return deaths_by_intervals


# Funkcia na spracovanie otázky
def process_question(question):
    print("Idem riešiť otázku: ", question)

    client = openai.Client(api_key=api_key)

    # Inicializácia klienta OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system","content": "You are an AI assistant that only answers questions about covid-19 data from "
                                         "a dataset that you have available. In the dataset, you have covid-19 deaths "
                                         "broken down by country over time."},
            {"role": "user", "content": f"Question: {question}. Does this question refer to covid-19 deaths?"}
        ]
    )

    gpt_response = response.choices[0].message.content
    print("tento response", gpt_response)

    if "áno" in gpt_response.lower() or "yes" in gpt_response.lower() or "Yes" in gpt_response.lower() or "Áno" in gpt_response.lower():
        # Extrahovanie názvu krajiny
        country_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract the country name from this question."},
                {"role": "user", "content": f"Question: {question}"}
            ]
        )
        country_name = country_response.choices[0].message.content
        print(country_name)

        # Extrahovanie intervalu z otázky
        interval_days = 30  # predvolený interval 30 dní
        interval_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract the interval in days from this question, if mentioned."},
                {"role": "user", "content": f"Question: {question}"}
            ]
        )
        try:
            interval_days = int(interval_response.choices[0].message.content.strip())
            print(f"Použitý interval: {interval_days} dní.")
        except ValueError:
            print(f"Nepodarilo sa extrahovať interval, používa sa predvolený interval {interval_days} dní.")


        # Extrahovanie kontinentu
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

        continent_name = continent.choices[0].message.content
        print("Continent name: ", continent_name)

        return search_from_datasets(country_name, continent_name, interval_days, question)
    else:
        return "I can't answer the question because it doesn't concern deaths from COVID-19."

# Funkcia na vyhľadávanie v datasete
def search_from_datasets(country, continent, question):
    path = "data"
    if continent == "Europe":
        path += "/europe/time_series_covid19_deaths_global.csv"
    elif continent == "Asia":
        path += "/asia/time_series_covid19_deaths_global.csv"
    elif continent == "Australia":
        path += "/australia/time_series_covid19_deaths_global.csv"
    elif continent == "North America":
        path += "/north_america/time_series_covid19_deaths_global.csv"
    elif continent == "South America":
        path += "/south_america/time_series_covid19_deaths_global.csv"
    elif continent == "Africa":
        path += "/africa/time_series_covid19_deaths_global.csv"

    # Načítanie datasetu
    dataset = pd.read_csv(path)
    if dataset is None:
        return f"Dataset pre kontinent {continent} nebol nájdený."

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

# Funkcia na vyhľadávanie v datasete
def search_from_datasets(country, continent, interval_days, question):
    path = "data"
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

    # Načítanie datasetu
    print(path)
    dataset = pd.read_csv(path)
    if dataset is None:
        return f"Dataset pre kontinent {continent} nebol nájdený."

    # Filtrovanie údajov pre konkrétnu krajinu
    if "Country/Region" not in dataset.columns:
        return f"Expected column 'Country/Region' was not found in the dataset."

    country_data = dataset[dataset["Country/Region"] == country]
    if country_data.empty:
        return f"No data found for country {country} in the dataset."

    # Rozdelenie údajov podľa zadaného intervalu
    deaths_by_intervals = calculate_deaths_in_intervals(country_data, interval_days)
    print(f"Deaths in {interval_days}-day intervals:")
    print(deaths_by_intervals)

    output_path = "deaths_by_intervals.csv"
    with open(output_path, 'w') as f:
        # Zapísať prvý riadok s názvami stĺpcov
        column_names = ["State"] + [f"{interval_days * (i + 1)}" for i in range(len(deaths_by_intervals))]
        f.write(",".join(column_names) + "\n")

        # Zapísať dáta: názov krajiny a hodnoty intervalov
        f.write(country + "," + ",".join(map(str, deaths_by_intervals)))

    print(f"Výsledky boli úspešne uložené do súboru: {output_path}")

    # Vrátenie odpovede ako pole číselných hodnôt
    # return deaths_by_intervals
    country_data = dataset[dataset["Country/Region"] == country]
    total_deaths = country_data.iloc[:, 4:].sum(axis=0).sum()
    print(f"Total deaths: {total_deaths}")


    prompt = f"""
    Question: {question}
    Country: {country}
    Deads in interval {interval_days} days: {deaths_by_intervals}
    Total Deaths: {total_deaths}
    You must provide a simple answer to the question asked based on the total number of deaths and the given interval.
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
    question = "How many people died from Covid-19 in Slovakia?"
    result = process_question(question)
    print(result)