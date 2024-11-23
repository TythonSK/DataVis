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


import os
import openai
from dotenv import load_dotenv

# Načítanie hodnôt z .env súboru
load_dotenv()

# Načítanie API kľúča z prostredia
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("API kľúč nie je nastavený v premennej prostredia 'OPENAI_API_KEY'")

# Inicializácia klienta OpenAI
client = openai.Client(api_key=api_key)

# Dopyt 1
stream_1 = client.chat.completions.create(
    model="gpt-4",  # Opravený model na existujúci
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)

# Spracovanie odpovedí pre dopyt 1
print("Odpoveď pre dopyt 1:")
for chunk in stream_1:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

# Dopyt 2
stream_2 = client.chat.completions.create(
    model="gpt-4",  # Používame rovnaký model pre druhý dopyt
    messages=[{"role": "user", "content": "Vies nacitavat datasety a spracovat ich?"}],
    stream=True,
)

# Spracovanie odpovedí pre dopyt 2
print("\nOdpoveď pre dopyt 2:")
for chunk in stream_2:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
