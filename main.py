from pynput import keyboard
from pynput.keyboard import Key,Controller
import pyperclip
import time

controller = Controller()

def fix_text(text):
    return text[::-1]

def fix_current_line():
    controller.press(Key.ctrl)
    controller.press(Key.shift)
    controller.press(Key.left)
    
    controller.release(Key.ctrl)
    controller.release(Key.shift)
    controller.release(Key.left)
    
def fix_selection():
    #1.Copy to Clipboard
    with controller.pressed(Key.ctrl):
        controller.tap('c')
    #2. get text from Clipboard
    time.sleep(0.2)
    text = pyperclip.paste()
    print(text)
    #3. fix the text
    fixed_text = fix_text(text)
    print(fixed_text)
    #4. copy back to clipboard
    pyperclip.copy(fixed_text)
    #5. insert text
    with controller.pressed(Key.ctrl):
        controller.tap('v')

def on_f9():
    fix_current_line()

def on_f10():
    fix_selection()
    print("f10 pressed")

with keyboard.GlobalHotKeys({
        '<120>': on_f9,
        '<121>': on_f10}) as h:
    h.join()