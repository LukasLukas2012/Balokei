#ich werde balt spracherkennung hinzufügen und vielleicht auch eine bessere stimmer ich nehme verbesserungsideen gerne entgegen

# ===== KONFIGURATION ===== #

user_name = "Lukas"
asistend_name = "Pixel"
sprechen = False       # ob antworten ausgesprochen oder nur ausgegeben werden also True/False
tabs_schliesen = True  # <-- EIN/AUS Schalter für automatisches Tab-Schließen # um kaos zu ferhindern sobalt du etwas neues öfnest wird das allte geschlossen

# ===== KONFIGURATION ===== #

# ===== Funktionen ===== # mehr kommen bald

#Sprachsteuerung (an/aus)
#Tab-Verwaltung (automatisches Schließen an/aus)
#Browser schließen
#Begrüßungen (Hallo, Hi, Hey, Moin)
#Lautstärkekontrolle (lauter, leiser, stumm, maximale Lautstärke)
#Helligkeitskontrolle (heller, dunkler, maximale Helligkeit)
#Zeit & Datum anzeigen
#Websites öffnen (Google, YouTube, Gmail, Facebook, Instagram)
#Wetter & Nachrichten
#Google-Suche
#Wikipedia-Suche
#Batterie-/Akkustand anzeigen
#Taschenrechner öffnen
#Witze erzählen
#Name erfragen (von Pixel und User)
#YouTube-Videos abspielen
#Programm beenden

# ===== Funktionen ===== # 

import sys
import subprocess

def install_package(package):
    try:
        import pip
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

package_mapping = {
    "pycaw": "pycaw",
    "screen_brightness_control": "screen_brightness_control",
    "requests": "requests",
    "bs4": "beautifulsoup4",
    "pytube": "pytube",
    "win32com.client": "pywin32",
    "psutil": "psutil"
}

for import_name, pip_name in package_mapping.items():
    try:
        __import__(import_name.split('.')[0])
        print(f"✓ {import_name} installiert")
    except ImportError:
        print(f"✗ Installiere {pip_name}...")
        install_package(pip_name)

# ===== IMPORTS =====
import datetime
import webbrowser
import re
import random
import os
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc
from pytube import Search
import win32com.client
import psutil

# ===== HILFSFUNKTIONEN =====
def speak(text):
    if sprechen:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Volume = 100
        speaker.Rate = 0.59
        speaker.Speak(text)

def antworten(text):
    print(f"{asistend_name}: {text}")
    speak(text)

def get_volume():
    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

# ===== LAUTSTÄRKE & HELLIGKEIT =====
def set_volume(level):
    vol = get_volume()
    if level == 0:
        vol.SetMute(1, None)
    else:
        vol.SetMute(0, None)
        vol.SetMasterVolumeLevelScalar(level / 100, None)

def änder_volume(delta):
    vol = get_volume()
    current = vol.GetMasterVolumeLevelScalar()
    vol.SetMasterVolumeLevelScalar(max(0.0, min(1.0, current + delta)), None)

def änder_helligkeit(delta):
    current = sbc.get_brightness()[0]
    sbc.set_brightness(max(0, min(100, current + delta)))
    print(f"Helligkeit: {max(0, min(100, current + delta))}")

# ===== SYSTEM FUNKTIONEN =====
def zeige_batterie():
    """Zeigt Akkustand an"""
    battery = psutil.sensors_battery()
    if battery:
        prozent = battery.percent
        plugged = battery.power_plugged
        status = "am Laden" if plugged else "nicht am Laden"
        antworten(f"Akku: {prozent}% ({status})")
    else:
        antworten("Keine Batterie gefunden (vermutlich Desktop-PC)")

# ===== BROWSER STEUERUNG =====
def schliesen():
    if tabs_schliesen:
        subprocess.run("taskkill /F /IM chrome.exe /IM msedge.exe /IM firefox.exe", 
                       shell=True, stderr=subprocess.DEVNULL)

def browser_schliesen():
    """Schließt Browser immer, unabhängig von tabs_schliesen Einstellung"""
    subprocess.run("taskkill /F /IM chrome.exe /IM msedge.exe /IM firefox.exe", 
                   shell=True, stderr=subprocess.DEVNULL)

# ===== HAUPTPROGRAMM =====
def main():
    global sprechen, tabs_schliesen
    
    # Begrüßung
    hr = datetime.datetime.now().hour
    gruß = f"Guten {'Morgen' if hr < 12 else 'Tag' if hr < 17 else 'Abend'}, {user_name}!"
    print(gruß)
    speak(gruß)
    antworten(f"Ich bin {asistend_name}, dein persönlicher Chatbot. Wie kann ich helfen?")
    
    while True:
        query = input("> ").lower().replace("bitte", "").replace("viel viel", "viel")
        
        if not query:
            continue
        
        # Sprachsteuerung
        if 'sprache aus' in query or 'sprachausgabe aus' in query:
            sprechen = False
            print(f"{asistend_name}: Sprachausgabe deaktiviert")
        elif 'sprache an' in query or 'sprachausgabe an' in query:
            sprechen = True
            antworten("Sprachausgabe aktiviert")
        
        # Tabs schließen
        elif 'tabs schließen aus' in query or 'tabs aus' in query:
            tabs_schliesen = False
            antworten("Tabs werden nicht mehr automatisch geschlossen")
        elif 'tabs schließen an' in query or 'tabs an' in query:
            tabs_schliesen = True
            antworten("Tabs werden wieder automatisch geschlossen")
        
        # Browser/Tabs schließen
        elif 'schließen' in query or 'schliesen' in query or 'browser schließen' in query:
            antworten("Schließe Browser...")
            browser_schliesen()
            antworten("Browser geschlossen")
        
        # Begrüßung
        elif re.search(r'\b(hallo|hi|hey|moin)\b', query):
            antworten("Hallo! Wie kann ich helfen?")
        
        # Lautstärke
        elif 'viel lauter' in query:
            änder_volume(0.2)
            antworten("Viel lauter")
        elif 'viel leiser' in query:
            änder_volume(-0.2)
            antworten("Viel leiser")
        elif 'lauter' in query:
            änder_volume(0.1)
            antworten("Lauter")
        elif 'leiser' in query:
            änder_volume(-0.1)
            antworten("Leiser")
        elif 'stumm' in query:
            set_volume(0)
            antworten("Stumm geschaltet")
        elif 'maximale lautstärke' in query:
            set_volume(100)
            antworten("Maximale Lautstärke")
        
        # Helligkeit
        elif 'viel heller' in query:
            änder_helligkeit(20)
            antworten("Viel heller")
        elif 'viel dunkler' in query:
            änder_helligkeit(-20)
            antworten("Viel dunkler")
        elif 'heller' in query:
            änder_helligkeit(10)
            antworten("Heller")
        elif 'dunkler' in query:
            änder_helligkeit(-10)
            antworten("Dunkler")
        elif 'maximale helligkeit' in query:
            sbc.set_brightness(100)
            antworten("Maximale Helligkeit")
        
        # Zeit & Datum
        elif 'zeit' in query or 'wie spät' in query:
            antworten(f"Es ist {datetime.datetime.now().strftime('%H:%M')} Uhr")
        elif 'datum' in query:
            antworten(f"Heute ist der {datetime.datetime.now().strftime('%d.%m.%Y')}")
        
        # Websites
        elif 'öffne google' in query:
            schliesen()
            antworten("Öffne Google...")
            webbrowser.open('https://www.google.com/')
        elif 'öffne youtube' in query:
            schliesen()
            antworten("Öffne YouTube...")
            webbrowser.open('https://www.youtube.com/')
        elif 'öffne gmail' in query:
            schliesen()
            antworten("Öffne Gmail...")
            webbrowser.open('https://www.gmail.com/')
        elif 'öffne facebook' in query:
            schliesen()
            antworten("Öffne Facebook...")
            webbrowser.open('https://www.facebook.com/')
        elif 'öffne instagram' in query:
            schliesen()
            antworten("Öffne Instagram...")
            webbrowser.open('https://www.instagram.com/')
        elif 'wetter' in query:
            schliesen()
            antworten("Zeige Wetter...")
            webbrowser.open('https://www.weather.com/')
        elif 'nachrichten' in query:
            schliesen()
            antworten("Zeige Nachrichten...")
            webbrowser.open('https://news.google.com/')
        
        # Suche
        elif 'suche google' in query or 'google suche' in query:
            schliesen()
            antworten("Was möchtest du suchen?")
            search = input("Suchbegriff: ")
            antworten("Suche...")
            webbrowser.open(f'https://www.google.com/search?q={search}')
        elif 'suche wikipedia' in query or 'wikipedia suche' in query:
            schliesen()
            antworten("Was auf Wikipedia suchen?")
            wiki = input("Suchbegriff: ")
            antworten(f"Öffne Wikipedia für '{wiki}'...")
            webbrowser.open(f"https://de.wikipedia.org/wiki/{wiki.replace(' ', '_')}")
        elif 'suche' in query:
            schliesen()
            suchbegriff = query.replace('suche', '').strip()
            if suchbegriff:
                antworten(f"Suche nach '{suchbegriff}' auf Google...")
                webbrowser.open(f'https://www.google.com/search?q={suchbegriff}')
            else:
                antworten("Was möchtest du suchen?")
                search = input("Suchbegriff: ")
                antworten("Suche...")
                webbrowser.open(f'https://www.google.com/search?q={search}')
        
        # Sonstiges
        elif 'wie geht es dir' in query:
            antworten("Mir geht es gut! Danke der Nachfrage.")
        elif 'batterie' in query or 'akku' in query:
            zeige_batterie()
        elif 'öffne rechner' in query or 'rechner öffnen' in query or 'taschenrechner' in query:
            antworten("Öffne Taschenrechner...")
            os.system('calc')
        elif 'witz' in query:
            witze = [
                "Warum können Geister so schlecht lügen? – Weil man durch sie hindurchsieht!",
                "Was macht ein Pirat am Computer? – Er drückt die Enter-Taste!",
                "Warum können Seeräuber keinen Kreis zeichnen? – Weil sie Pi raten!"
            ]
            antworten(random.choice(witze))
        elif 'wie heist du' in query:
            antworten(f"Ich heiße {asistend_name}")
        elif 'weist du wie ich heise' in query:
            antworten(f"Du heißt {user_name}")
        elif 'spiel ' in query or 'spiele ' in query:
            song = query.replace('spiel ', '').replace('spiele ', '').strip()
            if song:
                schliesen()
                antworten(f"Suche '{song}' auf YouTube...")
                search = Search(song)
                if search.results:
                    webbrowser.open(search.results[0].watch_url + "&autoplay=1&fs=1")
                else:
                    antworten(f"Kein Video gefunden für '{song}'")
            else:
                antworten("Was willst du spielen?")
        elif 'stop' in query or 'beenden' in query or 'halt' in query:
            antworten("Auf Wiedersehen!")
            schliesen()
            break
        else:
            antworten("Ich habe dich leider nicht verstanden")

if __name__ == "__main__":
    main()
