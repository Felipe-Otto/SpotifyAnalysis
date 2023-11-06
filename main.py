from utils import get_token, get_client_data, get_api_connection

# Obtaining Spotify API credentials from 'spotify_client.txt'
credentials = get_client_data()

# Obtaining client token
token = get_token(credentials['client_id'], credentials['client_secret'])

# Creating API connection
get_api_connection(token)

