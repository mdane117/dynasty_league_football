import requests
from bs4 import BeautifulSoup
import os
import csv

def scrape_season_stats(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        season_stats_table = soup.find('table', id='playerProfile-stats-careerTable')
        if season_stats_table:
            data = []
            for row in season_stats_table.find_all('tr')[1:]:
                columns = row.find_all('td')
                year = columns[0].text.strip()
                team = columns[1].text.strip()
                games_played = columns[2].text.strip()
                snap_count = columns[3].text.strip()
                snap_percent = columns[4].text.strip()
                pass_comp = columns[5].text.strip()
                pass_att = columns[6].text.strip()
                pass_yards = columns[7].text.strip()
                pass_tds = columns[8].text.strip()
                pass_ints = columns[9].text.strip()
                sacks = columns[10].text.strip()
                rush_att = columns[11].text.strip()
                rush_yards = columns[12].text.strip()
                rush_tds = columns[13].text.strip()
                fumbles = columns[14].text.strip()
                data.append([year, team, games_played, snap_count, snap_percent, pass_comp, pass_att, pass_yards, pass_tds, 
                    pass_ints, sacks, rush_att, rush_yards, rush_tds, fumbles])
            return data                
        else:
            print(f"Could not find {player_name}'s season stats table.")
    else:
        print(f"Failed to fetch the URL. Status code: {response.status_code}")

def export_to_csv(data, filename, output_folder):
    if data:
        filepath = os.path.join(output_folder, filename)
        is_file_empty = not (os.path.isfile(filepath) and os.path.getsize(filepath) > 0)
        with open(filepath, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if is_file_empty:
                writer.writerow(['player_id', 'player_name', 'player_url', 'position', 'year', 'team', 'games_played', 'snap_count', 'snap_percent', 'pass_comp', 'pass_att', 
                    'pass_yards', 'pass_tds', 'pass_ints', 'sacks', 'rush_att', 'rush_yards', 'rush_tds', 'fumbles'])
            writer.writerows(data)
        print(f"{player_name}'s data exported to {filename} successfully.")
    else:
        print("No data to export.")

if __name__ == "__main__":
    input_filename = "C:\\Users\\matth\\Desktop\\Python\\Web Scraper\\player_ranking_data\\qb_rankings.csv"
    output_folder = "C:\\Users\\matth\\Desktop\\Python\\Web Scraper\\player_season_data\\"
    output_filename = "qb_season_stats.csv"
    with open(input_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # skip header row
        for row in reader:
            rank, player_id, position, player_name, team, age, player_url = row
            scraped_data = scrape_season_stats(player_url)
            if scraped_data:
                for i in range(len(scraped_data)):
                    scraped_data[i] = [player_id, player_name, player_url, position] + scraped_data[i]

                export_to_csv(scraped_data, output_filename, output_folder)