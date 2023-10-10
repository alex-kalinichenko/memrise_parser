import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import logging
import os

current_folder = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(filename=os.path.join(current_folder, 'logging.log'), 
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Script started')

def get_username():
    with open(os.path.join(current_folder, 'username.txt'), 'r') as f:
        return f.read().strip()

def get_memrise_stats(username):
    url = f"https://www.memrise.com/user/{username}/"
    response = requests.get(url)
    if response.status_code != 200:
        logging.ERROR(f"Failed to fetch data for user {username}. HTTP Status Code: {response.status_code}")
        return None, None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    strong_tags = soup.find_all('strong')
    if len(strong_tags) < 3:
        logging.ERROR('Unexpected page structure')
        return None, None

    learned_words = strong_tags[2].get_text(strip=True).replace(',', '')
    points = soup.find('strong', class_='stat-value-xs').get_text(strip=True).replace(',', '')
    return int(learned_words), int(points)

def job():
    username = get_username()
    learned_words, points = get_memrise_stats(username)
    
    if learned_words is None or points is None:
        logging.ERROR('Failed to fetch stats')
        return

    today = datetime.date.today()
    data = {
        'Date': [today],
        'Learned Words': [learned_words],
        'Points': [points]
    }
    
    # Check if file exists
    file_path = os.path.join(current_folder, 'memrise_data.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=['Date', 'Learned Words', 'Points'])
        logging.ERROR('File not found')
    
    # Calculate daily activity
    if not df.empty:
        last_row = df.iloc[-1]
        words_diff = learned_words - last_row['Learned Words']
        points_diff = points - last_row['Points']
        print(f"Words learned today: {words_diff}")
        print(f"Points earned today: {points_diff}")
    
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    df.to_csv(file_path, index=False)

if __name__ == '__main__':
    job()
    logging.info('Script finished')
