import requests

url = "https://fantasy-api.formula1.com/partner_games/f1/players"

# Mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Origin": "https://fantasy.formula1.com",
    "Referer": "https://fantasy.formula1.com/"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # This will tell us if it's a 403 (Forbidden) or 404 (Not Found)
    data = response.json()
    print("Success! Data retrieved.")
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except Exception as err:
    print(f"An error occurred: {err}")
