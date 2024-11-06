import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import pygame
import time

class ReadContent:
    def __init__(self, source=None, is_url=True):
        """
        Initializes the class.
        
        :param source: URL or file path depending on the value of `is_url` (only necessary if `is_url` is True or False).
        :param is_url: If True, an article will be read from a URL, if False, it will be read from a file.
        """
        self.source = source
        self.is_url = is_url
        self.manual_text = None  # To store manual text if that option is used

    def get_text(self):
        """Gets the text content, either from a URL, a file, or manual text."""
        if self.manual_text:
            return self.manual_text
        elif self.is_url:
            return self.scrape_text()
        else:
            return self.get_text_from_file()

    def scrape_text(self):
        """Gets the text of an article from a URL."""
        try:
            # Get the page content
            response = requests.get(self.source)
            response.raise_for_status()  # Check that the request was successful

            # Parse the HTML and extract the text
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract only the text from the article's paragraphs
            paragraphs = soup.find_all('p')
            text = " ".join([p.get_text() for p in paragraphs])

            return text
        except:
            print("\nAn error occurred, please enter the URL correctly.")
            return None

    def get_text_from_file(self):
        """Gets the text from a file."""
        try:
            with open(self.source, 'r') as file:
                text = file.read()
            return text
        except FileNotFoundError:
            print("\nFile not found. Please enter a valid file path.")
            return None  # Returns None if the file is not found
        except Exception as e:
            print("\nAn error occurred:", e)
            return None

    def add_manual_text(self, text):
        """Allows the user to enter text manually."""
        self.manual_text = text

    def read_content(self):
        """Converts the text to audio using gTTS and plays it with pygame."""
        text = self.get_text()
        if text:
            # Convert the text to audio using gTTS
            tts = gTTS(text=text, lang='es')
            audio_file = "audio.mp3"
            tts.save(audio_file)

            # Initialize pygame and play the audio
            pygame.mixer.init() # Initialize the mixer
            pygame.mixer.music.load(audio_file) # Load the audio file
            pygame.mixer.music.play() # Play the audio

            # Keep the program running until the audio finishes
            while pygame.mixer.music.get_busy():
                time.sleep(1)
        else:
            print("Could not get the text to read.")
