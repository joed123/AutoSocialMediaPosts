This program uses the Reddit API to fetch stories from r/confessions and grabs Creative Commons gameplay videos from YouTube. It trims the video, adds AI narration using gTTS, and combines everything with MoviePy to create narrated short-form videos.

To run:

1. Make a Reddit app to grab a Reddit API key.
2. Get the Youtube Creative Commons API key.
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. python3 main.py     
