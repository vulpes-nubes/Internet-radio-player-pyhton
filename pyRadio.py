import sys
import vlc
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QSlider, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from io import BytesIO


class RadioPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        # VLC player instance
        self.player = vlc.MediaPlayer()

        # List to store previously used URLs
        self.url_list = []

    def init_ui(self):
        self.setWindowTitle('Internet Radio Player')

        # Input field for stream URL
        self.url_input = QComboBox(self)
        self.url_input.setEditable(True)
        self.url_input.setPlaceholderText('Enter stream URL (e.g., http://stream.laut.fm/lofi)')

        # Play button
        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.play_stream)

        # Stop button
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_stream)

        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        self.volume_slider.valueChanged.connect(self.set_volume)

        # Status label
        self.status_label = QLabel('Enter a URL to play...', self)

        # Metadata display
        self.title_label = QLabel('Song Title: N/A', self)
        self.album_art = QLabel(self)

        # Layout for GUI components
        layout = QVBoxLayout()
        layout.addWidget(self.url_input)
        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)

        # Add volume slider
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel('Volume:'))
        volume_layout.addWidget(self.volume_slider)
        layout.addLayout(volume_layout)

        layout.addWidget(self.status_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.album_art)

        self.setLayout(layout)
        self.setGeometry(300, 300, 500, 300)

    def play_stream(self):
        url = self.url_input.currentText()
        if url:
            # Add URL to the history if not already in the list
            if url not in self.url_list:
                self.url_input.addItem(url)
                self.url_list.append(url)

            # Set the media to play
            self.player.set_media(vlc.Media(url))
            self.player.play()

            # Update status and fetch metadata if available
            self.status_label.setText(f'Playing: {url}')
            self.fetch_metadata(url)
        else:
            self.status_label.setText('Please enter a valid URL.')

    def stop_stream(self):
        self.player.stop()
        self.status_label.setText('Stream stopped.')
        self.title_label.setText('Song Title: N/A')
        self.album_art.clear()

    def set_volume(self):
        volume = self.volume_slider.value()
        self.player.audio_set_volume(volume)

    def fetch_metadata(self, url):
        """Fetch metadata from the stream or API if available"""
        # Here we use requests to fetch metadata from the stream if available
        # For demo purposes, we simulate fetching metadata (title and album cover)
        try:
            # Fetch metadata (simulating metadata retrieval)
            title = "Unknown Song Title"
            album_cover_url = None

            # Example: You can fetch real metadata by parsing stream headers or using external APIs

            # Simulating album art from URL (replace this with real metadata)
            album_cover_url = 'https://www.example.com/path-to-album-cover.jpg'

            # Update title
            self.title_label.setText(f'Song Title: {title}')

            # Display album cover if URL is available
            if album_cover_url:
                response = requests.get(album_cover_url)
                pixmap = QPixmap()
                pixmap.loadFromData(BytesIO(response.content).read())
                self.album_art.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            else:
                self.album_art.clear()

        except Exception as e:
            self.status_label.setText('Failed to fetch metadata.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = RadioPlayer()
    player.show()
    sys.exit(app.exec_())
