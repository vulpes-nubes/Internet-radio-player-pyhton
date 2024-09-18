import os
import vlc
import ctypes
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QSlider, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from io import BytesIO
import requests

# Set the path to VLC libraries at runtime
if getattr(sys, 'frozen', False):
    # If running as a bundled executable (via PyInstaller)
    base_path = sys._MEIPASS
    libvlc_path = os.path.join(base_path, "libvlc.so")
    libvlccore_path = os.path.join(base_path, "libvlccore.so")
    ctypes.CDLL(libvlc_path)
    ctypes.CDLL(libvlccore_path)
else:
    # If running directly from Python, load VLC normally
    libvlc_path = ctypes.util.find_library('vlc')
    ctypes.CDLL(libvlc_path)

class RadioPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # VLC player instance
        self.player = vlc.MediaPlayer()

        # List to store previously used URLs
        self.url_list = []

    def init_ui(self):
        layout = QVBoxLayout()

        # URL input field
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter stream URL")
        layout.addWidget(self.url_input)

        # Play button
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_stream)
        layout.addWidget(self.play_button)

        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)
        layout.addWidget(self.volume_slider)

        # Label to display metadata (song title, artist, etc.)
        self.metadata_label = QLabel("Metadata will appear here", self)
        layout.addWidget(self.metadata_label)

        # Album art label
        self.album_art_label = QLabel(self)
        self.album_art_label.setFixedSize(200, 200)
        layout.addWidget(self.album_art_label)

        # Dropdown for previously used URLs
        self.url_dropdown = QComboBox(self)
        layout.addWidget(self.url_dropdown)

        self.setLayout(layout)
        self.setWindowTitle("Internet Radio Player")

    def play_stream(self):
        url = self.url_input.text()

        if url:
            self.player.set_mrl(url)
            self.player.play()

            # Add URL to the list of previously used URLs
            if url not in self.url_list:
                self.url_list.append(url)
                self.url_dropdown.addItem(url)

            # Try to fetch and display metadata (title, artist, etc.)
            self.fetch_metadata(url)

    def set_volume(self, value):
        self.player.audio_set_volume(value)

    def fetch_metadata(self, url):
        # Assume the stream URL might provide metadata such as song title and artist
        # Example: This could be handled via some custom stream metadata or headers
        try:
            # Simulate fetching metadata (in reality, this depends on the stream's metadata)
            metadata_url = f"{url}/metadata"  # Example URL pattern, adjust as needed
            response = requests.get(metadata_url)
            if response.status_code == 200:
                metadata = response.json()  # Assuming metadata is returned as JSON
                title = metadata.get("title", "Unknown Title")
                artist = metadata.get("artist", "Unknown Artist")
                album_art_url = metadata.get("album_art")

                # Update the metadata label
                self.metadata_label.setText(f"{title} - {artist}")

                # Fetch and display album art if available
                if album_art_url:
                    album_art_response = requests.get(album_art_url)
                    if album_art_response.status_code == 200:
                        album_art_data = album_art_response.content
                        pixmap = QPixmap()
                        pixmap.loadFromData(album_art_data)
                        self.album_art_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            else:
                self.metadata_label.setText("No metadata available.")
        except Exception as e:
            print(f"Error fetching metadata: {e}")
            self.metadata_label.setText("Error fetching metadata.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = RadioPlayer()
    player.show()
    sys.exit(app.exec_())
