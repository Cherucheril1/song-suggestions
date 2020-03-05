# song-recommender
A continuation of a project made at HackTX 2019. It recommends a song on Spotify.

Before you run:
The program needs the client id and client secret of a Spotify developer account.
Spotipy and Numpy should also be installed. Use:
pip install Numpy
pip install spotipy

The First Time:
The first time you run the code, A webpage will open up and the terminal will ask for a URL. Copy the URL of the webpage and paste it 
into the terminal and hit enter. Type CTRL and C at the same time into the terminal to close the program. This creates a cache file in the directory of your python file. You can save the file to avoid getting redirected again or you can delete it after you're done.

When the code runs like its supposed to, the window might say "Not responding", but it should load in a few seconds.

About:
The user gives a Spotify username, a playlist that they like, a playlist that they dislike, and a playlist that they want to explore. Using the data of the songs from the liked and disliked playlist, the program "learns" the user's musical taste. It then returns songs that it thinks are similar to the user's taste from the 3rd playlist that the user gave.
