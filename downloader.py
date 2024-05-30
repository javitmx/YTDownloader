from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog, QComboBox, QProgressBar
from PyQt5.QtGui import QFont
from pytube import YouTube
from pytube.cli import on_progress


class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setStyleSheet("background-color: #f0f0f0;")
        layout = QVBoxLayout(self)

        self.url_input = QLineEdit()
        layout.addWidget(QLabel("URL del video de YouTube:", self))
        layout.addWidget(self.url_input)

        self.ruta_input = QLineEdit()
        self.ruta_input.setReadOnly(True)
        layout.addWidget(QLabel("Ruta de guardado:", self))
        ruta_layout = QHBoxLayout()
        ruta_layout.addWidget(self.ruta_input)
        buscar_button = QPushButton("Buscar", self)
        buscar_button.setStyleSheet("background-color: #4CAF50; color: white;")
        buscar_button.clicked.connect(self.buscar_ruta)
        ruta_layout.addWidget(buscar_button)
        layout.addLayout(ruta_layout)

        self.nombre_input = QLineEdit()
        layout.addWidget(QLabel("Nombre del archivo (sin extensión):", self))
        layout.addWidget(self.nombre_input)

        self.calidad_combo = QComboBox()
        self.calidad_combo.addItems(["Máxima", "720p", "480p", "360p", "144p"])
        layout.addWidget(QLabel("Calidad de descarga:", self))
        layout.addWidget(self.calidad_combo)

        self.progressBar = QProgressBar()
        layout.addWidget(self.progressBar)

        self.descargar_button = QPushButton("Descargar", self)
        self.descargar_button.setStyleSheet(
            "background-color: #008CBA; color: white;")
        self.descargar_button.clicked.connect(self.descargar_video)
        layout.addWidget(self.descargar_button)

        # Establecer tamaño fijo de la ventana
        self.setFixedSize(500, 300)

    def buscar_ruta(self):
        ruta = QFileDialog.getExistingDirectory(
            self, "Seleccionar carpeta de descarga")
        if ruta:
            self.ruta_input.setText(ruta)

    def descargar_video(self):
        url = self.url_input.text()
        ruta = self.ruta_input.text()
        nombre = self.nombre_input.text()

        if url and ruta and nombre:
            try:
                yt = YouTube(url, on_progress_callback=self.show_progress)
                calidad = self.calidad_combo.currentText()
                if calidad == "Máxima":
                    video = yt.streams.filter(progressive=True).order_by(
                        'resolution').desc().first()
                else:
                    video = yt.streams.filter(
                        progressive=True, resolution=calidad, file_extension='mp4', subtype='mp4').first()
                    if not video:
                        video = yt.streams.filter(
                            resolution=calidad, file_extension='mp4', subtype='mp4').first()
                    if not video:
                        raise Exception(
                            "No se encontraron streams disponibles para la calidad seleccionada.")

                extension = 'mp4'
                video.download(output_path=ruta,
                               filename=nombre + '.' + extension)
                QMessageBox.information(self, "Éxito", "¡Descarga completada!")
                self.progressBar.setValue(0)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(
                self, "Advertencia", "Por favor, introduce la URL, la ruta de guardado y el nombre del archivo")

    def show_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progressBar.setValue(int(percentage))


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet("font-size: 16px; font-family: Arial;")
    window = DownloaderApp()
    window.show()
    app.exec_()
