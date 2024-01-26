import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_rankings(url, driver, username, password):
	webdriver_service = Service(ChromeDriverManager().install())
	options = Options()
	driver = webdriver.Chrome(service=webdriver_service, options=options)
	driver.get(url)
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table')))
	login_to_website(driver, username, password)
	page_source = driver.page_source
	soup = BeautifulSoup(page_source, 'html.parser')
	rankings_table = soup.find('table', attrs={'id': 'avgTable'})
	if rankings_table:
		print("Rankings found...")
		data = []
		rows = rankings_table.find_all('tr')[1:]
		for row in rows:
			columns = row.find_all('td')
			if columns:
				columns = row.find_all('td')
				rank = columns[0].text.strip()
				pos = columns[2].text.strip()
				player_name = columns[3].text.strip()
				player_url = columns[3].find('a')['href']
				team = columns[4].text.strip()
				age = columns[5].text.strip()
				pos = pos[:2] # removes the numbers following the player's position
				split_url = player_url.split('/')
				player_id = split_url[4]
				data.append([rank, player_id, pos, player_name, team, age, player_url])
		print("Data acquired.")
		driver.quit()
		return data
	else:
		print("Could not find rankings table.")
		driver.quit()
		return None

def login_to_website(driver, username, password):
	print("Logging into website...")
	username_field = driver.find_element(By.ID, 'user_login')
	username_field.send_keys(username)

	password_field = driver.find_element(By.ID, 'user_pass')
	password_field.send_keys(password)

	submit_button = driver.find_element(By.ID, 'wp-submit')
	submit_button.click()

	time.sleep(5) 	
	print("Login complete")

def export_to_csv(data, filename):
	if data:
		with open(filename, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['rank', 'player_id', 'position', 'player_name', 'team', 'age', 'player_url'])
			writer.writerows(data)
		print(f"Data exported to {filename} successfully.")
	else:
		print("No data to export.")

if __name__ == "__main__":
	# used with selenium
	webdriver_service = Service(ChromeDriverManager().install())
	options = Options()
	driver = webdriver.Chrome(service=webdriver_service, options=options)

	position_urls = [
		"https://dynastyleaguefootball.com/rankings/qb-rankings/",
		"https://dynastyleaguefootball.com/rankings/rb-rankings/",
		"https://dynastyleaguefootball.com/rankings/wr-rankings/",
		"https://dynastyleaguefootball.com/rankings/te-rankings/"
	]
	positions = ['qb', 'rb', 'wr', 'te']

	username = "" # Add username
	password = "" # Add password
	
	for url, position in zip(position_urls, positions):
		scraped_data = scrape_rankings(url, position, username, password)
		if scraped_data:
			output_folder = "" # Add filepath to output folder
			export_to_csv(scraped_data, f"{position}_rankings.csv", output_folder)
