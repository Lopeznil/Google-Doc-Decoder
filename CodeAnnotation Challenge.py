import requests
from bs4 import BeautifulSoup

def print_secret_message(doc_url):
    # Fetch the document content
    response = requests.get(doc_url)
    response.raise_for_status()  # Check for request errors

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table in the document (assuming it's the first or only table)
    table = soup.find('table')

    # Initialize a list to hold the table rows
    data = []

    # Iterate through the rows of the table, skipping the first row (header)
    rows = table.find_all('tr')[1:]  # Skip the header row
    for row in rows:
        # Get the cells (td) in each row
        cells = row.find_all('td')
        if len(cells) >= 3:
            try:
                # Append the row data as a dictionary
                data.append({
                    'x-coordinate': int(cells[0].get_text().strip()),
                    'character': cells[1].get_text().strip(),
                    'y-coordinate': int(cells[2].get_text().strip())
                })
            except ValueError as e:
                print(f"Skipping row due to value error: {e}")

    # Determine the size of the grid
    if data:
        max_row = max(item['y-coordinate'] for item in data)
        max_col = max(item['x-coordinate'] for item in data)
        grid = [[' ' for _ in range(max_col + 1)] for _ in range(max_row + 1)]

        # Fill the grid with characters
        for item in data:
            grid[item['y-coordinate']][item['x-coordinate']] = item['character']

        # Print the grid (reveals the secret message)
        for line in grid:
            print(''.join(line))
    else:
        print("No valid data found in the table.")

# Example usage:
print_secret_message('https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub')
