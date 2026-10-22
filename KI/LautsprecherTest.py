import os

# Der Text, den Korex sprechen soll
text = "Hallo, ich bin Korex der Roboter"

print("Korex spricht jetzt...")

# Der Befehl führt den Sprachausgabe-Befehl im System aus
# '-v de' sorgt dafür, dass die deutsche Stimme verwendet wird
os.system(f'espeak-ng -v de "{text}"')

print("Ausgabe beendet.")