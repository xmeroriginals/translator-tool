import os
import sys
import requests
import json
import keyboard
import pystray
from pystray import MenuItem as item
from PIL import Image
import pyperclip
from playsound3 import playsound
import threading

def get_asset_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

icon_path = get_asset_path("assets/translator.png")
sound_path = get_asset_path("assets/completed.mp3")

languages = {
    "Turkish": "tr",
    "English": "en",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Russian": "ru",
    "Chinese": "zh-cn"
}

current_language = "en"

def translate_text(text, target_language):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={requests.utils.quote(text)}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        translated_text = data[0][0][0]
        return translated_text
    else:
        raise Exception(f"Error")

def run_translator():
    while True:
        keyboard.wait('ctrl+alt+c')
        text = pyperclip.paste()
        if text:
            try:
                translated_text = translate_text(text, current_language)
                pyperclip.copy(translated_text)
                playsound(sound_path)
            except Exception as e:
                print(f"Error {e}")
        else:
            print("Empty")

def set_language(icon, item):
    global current_language
    current_language = languages[item.text]
    print(f"Language {item.text}")

def on_exit(icon, item):
    os._exit(0)

def create_system_tray_icon():
    menu_items = [item(lang_name, lambda _, lang_name=lang_name: set_language(None, lang_name)) for lang_name in languages.keys()]
    menu_items.append(item('Exit', on_exit))
    
    image = Image.open(icon_path)
    icon = pystray.Icon("Translator", image, "Translator", pystray.Menu(*menu_items))
    icon.run()

if __name__ == "__main__":
    threading.Thread(target=create_system_tray_icon, daemon=True).start()
    run_translator()
