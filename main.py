import requests
from bs4 import BeautifulSoup


def get_scorecard(url):
	# Send an HTTP request and get the webpage content
	response = requests.get(url)

	# Check for successful response
	if response.status_code == 200:
		# Parse the HTML content
		soup = BeautifulSoup(response.content, 'html.parser')

		teams = soup.find_all('span', class_='ds-text-title-xs ds-font-bold ds-capitalize')
		teams = [team.text.strip() for team in teams]

		tables = soup.find_all('table')
		c = 0

		# Extract table data
		for table in tables:
			batpos = 0
			data = []
			table_name = table.find('th')
			if table_name:
				if table_name.text.strip() not in ["BATTING", "BOWLING"]:
					continue
				print(table_name.text.strip())
				for row in table.find_all('tr'):
					row_data = []
					for cell in row.find_all('td'):
						cell_text = cell.text.strip()
						if cell_text:
							row_data.append(cell_text)
					if row_data:
						if len(row_data) < 4:
							continue
						if table_name.text.strip() == "BATTING":
							if row_data[1] == 'not out':
								row_data[1] = 'not_out'
							else:
								row_data[1] = 'out'
							row_data.insert(0, batpos+1)
							batpos+=1

						row_data.insert(0, f'{teams[0]} Vs {teams[1]}')
						row_data.insert(1, teams[c%2])
						data.append(row_data)
				c+=1

				# Print or process the scraped data (list of lists)
				for i in data:
					print(i)
				print()


	else:
		print(f"Error: Failed to retrieve the webpage. Status code: {response.status_code}")


if __name__ == '__main__':
	url = 'https://www.espncricinfo.com/series/indian-premier-league-2024-1410320/kolkata-knight-riders-vs-sunrisers-hyderabad-final-1426312/full-scorecard'
	get_scorecard(url)