#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Test script to use SoundToTextLocal and trigger recognition with spacebar

import os
from SoundToTextLocal import SoundToText
from pynput import keyboard

# 实例化 SoundToText 类
sound_to_text = SoundToText()

def on_press(key):
    try:
        # 检测空格键
        if key == keyboard.Key.space:
            print("Space pressed. Starting recognition...")
            result = sound_to_text.recognize("./requestSound.wav")
            print(f"Recognition Result:\n{result}")
        # 检测退出键 'q'
        elif key.char == 'q':
            print("Quitting program.")
            return False
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Model initialized. Press SPACE to recognize './requestSound.wav', or 'q' to quit.")

    # 使用 pynput 监听按键
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()