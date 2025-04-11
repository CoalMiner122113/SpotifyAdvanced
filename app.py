import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Spotify Advanced Search",
    page_icon="🎵",
    layout="wide"
)

# Title and description
st.title("🎵 Spotify Advanced Search")
st.markdown("""
    Search for songs using advanced criteria like composer, artist, and more!
""")

# Initialize Spotify client
@st.cache_resource
def init_spotify():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))

# Create search form
with st.form("search_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        track_name = st.text_input("Track Name")
        artist = st.text_input("Artist")
    
    with col2:
        composer = st.text_input("Composer")
        year = st.number_input("Year", min_value=1900, max_value=2024, step=1)
    
    search_button = st.form_submit_button("Search")

# Display results
if search_button:
    try:
        sp = init_spotify()
        # Construct search query
        query = ""
        if track_name:
            query += f"track:{track_name} "
        if artist:
            query += f"artist:{artist} "
        if composer:
            query += f"composer:{composer} "
        if year:
            query += f"year:{year} "
        
        results = sp.search(q=query, type='track', limit=10)
        
        if results['tracks']['items']:
            st.subheader("Search Results")
            for track in results['tracks']['items']:
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(track['album']['images'][0]['url'], width=100)
                with col2:
                    st.write(f"**{track['name']}**")
                    st.write(f"Artist: {', '.join([artist['name'] for artist in track['artists']])}")
                    st.write(f"Album: {track['album']['name']}")
                    st.write(f"Release Date: {track['album']['release_date']}")
                    st.audio(track['preview_url'] if track['preview_url'] else None)
                st.divider()
        else:
            st.warning("No results found. Try different search criteria.")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Make sure you have set up your Spotify API credentials in the .env file") 