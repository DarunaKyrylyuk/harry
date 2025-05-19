import sqlite3
import json
from datetime import datetime

# Завантаження JSON
with open("data/episods.json", "r", encoding="utf-8") as f:
    anime_data = json.load(f)

# Підключення до бази даних
conn = sqlite3.connect("anime.db")
cursor = conn.cursor()

# Функція для вставки аніме, сезонів і серій
def insert_anime():
    for key, anime in anime_data.items():
        cursor.execute('''
            INSERT INTO anime (data, name, description, cover, genres)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            anime["title"],
            anime["description"],
            anime["cover"],
            ",".join(anime["genres"])  # Без перевірки — вставляємо як є
        ))
        anime_id = cursor.lastrowid

        for season in anime["seasons"]:
            cursor.execute('''
                INSERT INTO seasons (anime_id, name)
                VALUES (?, ?)
            ''', (anime_id, season["seasonTitle"]))
            season_id = cursor.lastrowid

            for i in range(1, season["episodes"] + 1):
                cursor.execute('''
                    INSERT INTO series (season_id, video, name)
                    VALUES (?, ?, ?)
                ''', (
                    season_id,
                    f"videos/{key}/episode_{i}.mp4",  # Шаблон шляху до відео
                    f"Серія {i}"
                ))

insert_anime()
conn.commit()
conn.close()
print("Імпорт завершено!")
