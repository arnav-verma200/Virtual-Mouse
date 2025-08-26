# 🖐️ Hand Gesture Virtual Mouse & Keyboard

Control your computer using just your hands ✋🖱️⌨️.
This project uses **MediaPipe** and **OpenCV** to track hand landmarks, combined with **pynput** and **pyautogui** to simulate real mouse and keyboard actions.

It includes:

* **Virtual Mouse** – Move the pointer, click, and scroll with simple pinch gestures.
* **Virtual Keyboard** – Type letters, space, backspace, and enter by hovering your fingertip over an on-screen keyboard.

---

## ✨ Features

### 🖱️ Virtual Mouse

* Move the mouse using your **palm center**.
* Smooth cursor movement with built-in filtering.
* Perform common actions with **pinch gestures**:

  * 👉 **Thumb + Index** → Left Click
  * 👉 **Thumb + Middle** → Right Click
  * 👉 **Thumb + Ring** → Scroll Up
  * 👉 **Thumb + Pinky** → Scroll Down

### ⌨️ Virtual Keyboard

* On-screen keyboard layout (A–Z + Space, Backspace, Enter).
* **Hover your index fingertip** over a key to highlight it.
* Hold for **1 second** to “press” the key.
* Typed text is displayed on screen **and** entered into the system (via `pynput`).

---

## ⚙️ Requirements

* Python **3.8+**
* Install dependencies with:

```bash
pip install -r requirements.txt
```

`requirements.txt` contains:

```
opencv-python
mediapipe
pynput
pyautogui
```

---

## 📂 Project Structure

```
├── virtual_mouse.py       # Hand gesture-based mouse controller
├── virtual_keyboard.py    # On-screen keyboard controlled by hand gestures
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

---

## ▶️ Usage

### Run Virtual Mouse

```bash
python virtual_mouse.py
```

### Run Virtual Keyboard

```bash
python virtual_keyboard.py
```

➡️ Press **Q** anytime to quit.

---

## 🔧 Tips

* Use in **good lighting** for accurate hand tracking.
* Works best with **one hand visible**.
* Adjust `pinch_threshold` (mouse) or **selection delay** (keyboard) if gestures feel too sensitive or slow.

---

## 🚀 Future Improvements

* ✅ Multi-hand support
* ✅ Extra mouse gestures (drag & drop, copy-paste)
* ✅ Smarter keyboard (auto-suggest / predictive typing)
* ✅ GUI overlay instead of drawn rectangles

---

## 🌟 Conclusion

This project shows how computer vision and hand-tracking can make human–computer interaction more natural.
It’s a simple start, but with more gestures, AI-powered text prediction, and multi-hand support, it can grow into a fully functional **touchless control system**.

If you like this project, ⭐ the repo and feel free to fork, improve, or share your own ideas! 🚀

---
