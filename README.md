# ✍️ Air Finger Drawing App using MediaPipe and OpenCV

This project is a **real-time finger drawing application** using your webcam and hand gestures. It uses **MediaPipe** to track your hand landmarks and **OpenCV** to draw strokes on a virtual canvas — like drawing in the air!

> ✅ This version uses CPU only and runs smoothly on most systems.

---

## 📸 Demo

*(Add your own GIF or image demo here)*  
![demo](https://your-link.com/demo.gif)

---

## 🧠 How It Works

- 📷 **OpenCV** captures real-time video from your webcam.
- 🖐️ **MediaPipe** detects your hand and identifies **21 landmarks**, including your index finger tip.
- 🖊️ When only the index finger is raised, it enters "draw mode" and tracks finger movement.
- 🧠 Draws lines using OpenCV on a separate canvas and merges it with the live feed.

---

## ✅ Features

- 🎨 Draw with your index finger
- 🌈 Change pen colors (`R`, `G`, `B`, `M`)
- ➕ Increase/decrease brush size
- 🧽 Clear canvas (`C`)
- 💾 Save drawing as PNG (`S`)
- 👋 Easy to use gesture recognition (1 finger = draw, others = pause)

---

## 🛠 Requirements

- Python 3.7 – 3.11
- Webcam
- No GPU required

### 📦 Install dependencies:

```bash
pip install mediapipe opencv-python numpy
