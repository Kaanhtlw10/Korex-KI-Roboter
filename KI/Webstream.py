import io
from flask import Flask, Response, render_template_string
from picamera2 import Picamera2

app = Flask(__name__)

# Kamera konfigurieren und starten
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

# Einfache HTML-Oberfläche für den Browser
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Raspberry Pi Kamera Live-Übertragung</title>
    <style>
        body { font-family: sans-serif; text-align: center; background: #222; color: #fff; margin-top: 50px; }
        img { border: 6px solid #fff; border-radius: 12px; }
    </style>
</head>
<body>
    <h1>Raspberry Pi Kamera Live-Übertragung (Modul 3)</h1>
    <img src="/video_feed" width="1000" height="600">
</body>
</html>
"""

def generate_frames():
    while True:
        # Bild in den Arbeitsspeicher als JPEG aufnehmen
        stream = io.BytesIO()
        picam2.capture_file(stream, format='jpeg')
        frame = stream.getvalue()
        
        # Frame im MJPEG-Format an den Browser senden
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Startet den Server im lokalen Netzwerk auf Port 5000
    app.run(host='0.0.0.0', port=5000, debug=False)