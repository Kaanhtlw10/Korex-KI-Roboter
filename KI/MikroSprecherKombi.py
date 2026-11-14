import os
import speech_recognition as sr

# Initialisiere den Recognizer
r = sr.Recognizer()

print("=== Korex ist bereit! ===")
print("Drücke jederzeit im Terminal **Strg + C**, um das Programm zu beenden.\n")
os.system(f'espeak-ng -v de "Hallo, ich bin Korex der Roboter, wie kann ich dir helfen?"')

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

        #selber geschriebene Befehlantworten
        if "wie geht es dir" in text.lower():
            antwort = "Mir geht es gut, wie geht es dir?"
            print(f"Korex antwortet: {antwort}")
            os.system(f'espeak-ng -v de "{antwort}"')
           

        if "wie heißt du" in text.lower():
            antwort1 = "Ich heiße Korex der Roboter, ich bin ein KI integrierter smart Roboter"
            print(f"Korex antwortet: {antwort1}")
            os.system(f'espeak-ng -v de "{antwort1}"')
            

        if "was ist der datum von heute" in text.lower() :
            antwort2 = "Schau in den Kalender"
            print(f"Korex antwortet: {antwort2}")
            os.system(f'espeak-ng -v de "{antwort2}"')
        

        if "wie viel uhr ist es" in text.lower() :
            antwort3 = "Schau auf die Uhr"
            print(f"Korex antwortet: {antwort3}")
            os.system(f'espeak-ng -v de "{antwort3}"')
          

        if "wie ist das wetter heute" in text.lower():
            antwort4 = "Schau in die Wetter App rein"
            print(f"Korex antwortet: {antwort4}")
            os.system(f'espeak-ng -v de "{antwort4}"')
            
        
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