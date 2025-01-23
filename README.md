# Spotify Insights 🎵

A web application that leverages the Spotify Web API to provide personalized music insights, recommendations, and playlist generation. This project showcases skills in API integration, data visualization, and web application development.

---

## Features 🌟

- **User Authentication**: Securely log in with Spotify using OAuth.
- **Top Listening Stats**: View your top artists, tracks, and genres over different time periods.
- **Music Recommendations**: Receive personalized song and artist recommendations.
- **Mood-Based Playlists**: Generate playlists based on your mood (e.g., happy, calm, energetic).
- **Visualizations**: Interactive graphs to analyze your listening habits.

---

## Technologies Used 🛠️

- **Backend**: Python, Flask
- **Frontend**: React.js (optional for future development)
- **Data Analysis**: Spotipy, pandas
- **Visualization**: Plotly, Matplotlib
- **Hosting**: (Optional: AWS/GCP/Heroku)
- **Spotify API**: Fetch user-specific data and control playback

---

## Getting Started 🚀

### Prerequisites
- Python 3.8+
- Spotify Developer Account
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/spotify-insights.git
   cd spotify-insights# spotify-insights

2.	Set up a virtual environment:
      python3 -m venv venv
      source venv/bin/activate  # On macOS/Linux

3.	Install dependencies:
      pip install -r requirements.txt

4.	Configure environment variables in a .env file:
      SPOTIFY_CLIENT_ID=<your-client-id>
      SPOTIFY_CLIENT_SECRET=<your-client-secret>
      SPOTIFY_REDIRECT_URI=http://localhost:8080/callback

5.	Run the application:
      python3 app.py

6.	Visit the app in your browser at http://localhost:8080.

Future Enhancements 🔮
-	Add social sharing features (e.g., share your stats with friends).
-	Integrate AI to suggest music based on text input (e.g., “I feel happy”).
-	Implement caching to improve performance.

Contributing 🤝

Contributions are welcome! Feel free to fork this repository, make your changes, and submit a pull request.

License 📜

This project is licensed under the MIT License.

Acknowledgments 💖
-	Thanks to Spotify for providing the API.
-	Inspiration from Spotify Wrapped.