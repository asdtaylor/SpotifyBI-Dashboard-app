import os
import requests
import pandas as pd
from urllib.parse import quote


# Initialize your client ID and client secret from Spotify Developer dashboard. Stored locally as environment variables.
CLIENT_ID = os.environ.get('Spotify_CLIENT_ID') 
CLIENT_SECRET  = os.environ.get('Spotify_CLIENT_SECRET')

# Fetch an access token from Spotify
auth_response = requests.post(
    'https://accounts.spotify.com/api/token',
    data={'grant_type': 'client_credentials', 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
)
auth_data = auth_response.json()
access_token = auth_data['access_token']

# Prepare headers for API requests
headers = {'Authorization': f'Bearer {access_token}'}

# Load existing CSV file into a dataframe
df = pd.read_csv('Spotify2023.csv', encoding='ISO8859-1')

# Create an empty list to store cover URLs
cover_urls = []

# Loop through each row in the DataFrame to search for tracks on Spotify
for _, row in df.iterrows():
    track_name = row['track_name']
    artist_name = row['artist(s)_name']
    
    # URL encode the query string to handle special characters
    query = quote(f"track:{track_name} artist:{artist_name}")
    
    # Send the API request with the correct query parameter
    search_response = requests.get(f"https://api.spotify.com/v1/search?q={query}&type=track", headers=headers)
    
    # Check the status code of the response
    if search_response.status_code != 200:
        print(f"Failed to get data for query '{query}': {search_response.content}")
        cover_url = 'API Error'
    else:
        search_data = search_response.json()
        try:
            cover_url = search_data['tracks']['items'][0]['album']['images'][0]['url']
        except (KeyError, IndexError):
            print(f"No data found for query '{query}': {search_data}")
            cover_url = 'Not Found'
        
    cover_urls.append(cover_url)

# Add the list of cover URLs as a new column to the dataframe
df['cover_url'] = cover_urls

# Save the updated dataframe as a new CSV file
df.to_csv('updated_spotify_data.csv', index=False)
