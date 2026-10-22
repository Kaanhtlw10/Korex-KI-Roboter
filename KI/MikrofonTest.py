import speech_recognition as sr

# Initialisiere den Recognizer
r = sr.Recognizer()

# Verwende das Standard-Mikrofon als Quelle
with sr.Microphone() as source:
    print("Mikrofon ist bereit. Bitte sprich etwas...")
    
    # Optional: Hintergrundgeräusche kurz anpassen
    r.adjust_for_ambient_noise(source, duration=1)
    
    # Höre auf die Eingabe des Benutzers
    audio = r.listen(source)

print("Verarbeite Audio...")

try:
    # Spracherkennung auf Deutsch (erfordert eine Internetverbindung)
    text = r.recognize_google(audio, language="de-DE")
    print(f"\nDu hast gesagt: {text}")

except sr.UnknownValueError:
    print("Das Audio konnte nicht verstanden werden.")
except sr.RequestError as e:
    print(f"Fehler beim Verbinden mit dem Dienst; {e}")



