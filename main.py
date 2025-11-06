from pynput import keyboard
from pynput.keyboard import Key,Controller
import pyperclip
import time
import httpx
from string import Template

controller = Controller()

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_CONFIG={
    "model": "mistral",
    "keep_alive" : "5m",
    "stream" : False
}

PROMPT_TEMPLATE = Template(
    """Fix all typos and casing and puncation in this text,but preserve all new line characters:
     
     $text

     Return only the corrected text,don't include a preamble.
           
    """
)

def fix_text(text):
    prompt = PROMPT_TEMPLATE.substitute(text=text)
    try :
        response = httpx.post(OLLAMA_ENDPOINT,
                            json={"prompt" : prompt,**OLLAMA_CONFIG},
                            headers={"Content-Type":"application/json"},
                            timeout=10)
        print(response.text)
        if response.status_code !=   200:
            return text
        return response.json()["response"].strip()
    except Exception as e:
        print("Error : ",e)
        return text    

def fix_current_line():
    controller.press(Key.ctrl)
    controller.press(Key.shift)
    controller.press(Key.left)
    
    controller.release(Key.ctrl)
    controller.release(Key.shift)
    controller.release(Key.left)
    fix_selection()
    
def fix_selection():
    #1.Copy to Clipboard
    with controller.pressed(Key.ctrl):
        controller.tap('c')

    #2. get text from Clipboard
    time.sleep(0.1)
    text = pyperclip.paste()

    #3. fix the text
    if not text:
        return
    fixed_text = fix_text(text)
    print(fixed_text)
    if not fixed_text:
        return
    
    #4. copy back to clipboard
    pyperclip.copy(fixed_text)
    time.sleep(0.1)
    
    #5. insert text
    with controller.pressed(Key.ctrl):
        controller.tap('v')

def on_f9():
    fix_current_line()

def on_f10():
    fix_selection()

with keyboard.GlobalHotKeys({
        '<120>': on_f9,
        '<121>': on_f10}) as h:
    h.join()