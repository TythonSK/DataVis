# import os
# import openai
# from dotenv import load_dotenv
#
# # Načítanie hodnôt z .env súboru
# load_dotenv()
#
# # Načítanie API kľúča z prostredia
# api_key = os.getenv('OPENAI_API_KEY')
#
# if not api_key:
#     raise ValueError("API kľúč nie je nastavený v premennej prostredia 'OPENAI_API_KEY'")
#
# client = openai.Client(api_key=api_key)
#
# stream = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Say this is a test"}],
#     stream=True,
# )
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")

#############################################################
# import os
# import openai
# from dotenv import load_dotenv
#
# # Načítanie hodnôt z .env súboru
# load_dotenv()
#
# # Načítanie API kľúča z prostredia
# api_key = os.getenv('OPENAI_API_KEY')
#
# if not api_key:
#     raise ValueError("API kľúč nie je nastavený v premennej prostredia 'OPENAI_API_KEY'")
#
# # Inicializácia klienta OpenAI
# client = openai.Client(api_key=api_key)
#
# # Dopyt 1
# stream_1 = client.chat.completions.create(
#     model="gpt-4",  # Opravený model na existujúci
#     messages=[{"role": "user", "content": "Say this is a test"}],
#     stream=True,
# )
#
# # Spracovanie odpovedí pre dopyt 1
# print("Odpoveď pre dopyt 1:")
# for chunk in stream_1:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")
#
# # Dopyt 2
# stream_2 = client.chat.completions.create(
#     model="gpt-4",  # Používame rovnaký model pre druhý dopyt
#     messages=[{"role": "user", "content": "Napis ahoj."}],
#     stream=True,
# )
#
# # Spracovanie odpovedí pre dopyt 2
# print("\nOdpoveď pre dopyt 2:")
# for chunk in stream_2:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")
###########################################################

import os
import openai
import csv
import pandas as pd
from dotenv import load_dotenv

# Načítanie hodnôt z .env súboru
load_dotenv()

# Načítanie API kľúča z prostredia
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("API kľúč nie je nastavený v premennej prostredia 'OPENAI_API_KEY'")

# Inicializácia OpenAI klienta
openai.api_key = api_key

# Načítanie datasetu
input_file = 'data/time_series_covid19_deaths_global.csv'
output_file = 'output_results.csv'

# Načítanie CSV pomocou pandas
df = pd.read_csv(input_file)

# Rozdelenie stĺpcov na metaúdaje a dátové hodnoty
meta_columns = ['Province/State', 'Country/Region', 'Lat', 'Long']
data_columns = [col for col in df.columns if col not in meta_columns]

# Otvorenie výstupného súboru na zapisovanie
with open(output_file, mode='w', encoding='utf-8', newline='') as outputfile:
    fieldnames = ['id', 'input_text', 'response']
    writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterácia cez riadky datasetu
    for index, row in df.iterrows():
        country = row['Country/Region']
        state = row['Province/State']
        latitude = row['Lat']
        longitude = row['Long']

        # Hodnoty podľa dátumu
        date_values = row[data_columns]
        input_text = (
            f"Krajina: {country}, Štát: {state}, Súradnice: ({latitude}, {longitude}). "
            f"Hodnoty úmrtí podľa dátumov:\n" +
            "\n".join([f"{date}: {value}" for date, value in date_values.items()])
        )

        print(f"Spracovávam: {input_text}")

        # Volanie OpenAI API
        try:
            client = openai.Client(api_key=api_key)
            response = client.chat.completions.create(
            # response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": input_text}],
                temperature=0.7
            )
            output_text = response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Chyba pri spracovaní: {e}")
            output_text = "Error: Unable to process."

        # Zapísanie výsledku do výstupného CSV súboru
        writer.writerow({'id': index, 'input_text': input_text, 'response': output_text})

print(f"Spracovanie dokončené. Výstup uložený v {output_file}.")

