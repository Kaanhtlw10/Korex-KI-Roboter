import os
import speech_recognition as sr

# Initialisiere den Recognizer
r = sr.Recognizer()

print("=== Korex ist bereit! ===")
print("Drücke jederzeit im Terminal **Strg + C**, um das Programm zu beenden.\n")

# Endlosschleife: Läuft, bis du sie abbrichst
while True:
    try:
        # Verwende das Standard-Mikrofon als Quelle
        with sr.Microphone() as source:
            print("Mikrofon ist bereit. Bitte sprich etwas...")
            
            # Hintergrundgeräusche kurz anpassen (verkürzt auf 0.5 Sekunden für schnelleres Reagieren)
            r.adjust_for_ambient_noise(source, duration=0.5)
            
            # Höre auf die Eingabe des Benutzers
            audio = r.listen(source)

        print("Verarbeite Audio...")

        # Spracherkennung auf Deutsch
        text = r.recognize_google(audio, language="de-DE")
        print(f"Du hast gesagt: {text}")
        
        # Optional: Wenn du das Programm per Sprachbefehl stoppen willst
        if "stopp" in text.lower() or "beenden" in text.lower():
            print("Programm wird beendet...")
            os.system('espeak-ng -v de "Tschüss!"')
            break

        # Den erkannten Text über den Lautsprecher ausgeben
        print("Korex spricht jetzt...")
        os.system(f'espeak-ng -v de "{text}"')
        print("Ausgabe beendet.\n" + "-"*30 + "\n")

    except sr.UnknownValueError:
        print("Das Audio konnte nicht verstanden werden. Versuche es noch einmal.\n")
    except sr.RequestError as e:
        print(f"Fehler beim Verbinden mit dem Dienst: {e}\n")
    except KeyboardInterrupt:
        # Fängt den Abbruch ab, wenn du Strg+C drückst
        print("\nProgramm durch Benutzer beendet. Auf Wiedersehen!")
        break