
# 🎥 LAN Audio & Video Streaming App

> A cross-platform Python desktop application that captures microphone and webcam input from one machine (server) and streams it in real-time to another machine (client) over TCP on port 443.

---

## 📌 Purpose

The goal is to enable secure and reliable audio-video streaming across machines within the same LAN, even when the client device is behind a strict firewall that blocks most incoming connections. By streaming over TCP port 443, we ensure high compatibility with restrictive network environments.

---

## 🎯 Goals

### Minimum Viable Product (MVP)
- [ ] Capture webcam video from the server using OpenCV
- [ ] Capture microphone audio from the server using `sounddevice`
- [ ] Stream audio and video to a client over TCP on port 443
- [ ] Display video in a GUI window on the client
- [ ] Play audio in real-time on the client

### Stretch Goals
- [ ] Add GUI controls for connecting/disconnecting, status, and volume
- [ ] Compress and decompress audio/video for lower latency
- [ ] Add basic encryption (SSL or symmetric encryption)
- [ ] Multi-client support

### Personal Learning Goals
- [ ] Deepen understanding of socket programming and audio/video encoding
- [ ] Gain experience with cross-platform GUI development (e.g. PyQt, Dear PyGui)
- [ ] Improve concurrency handling using `threading` or `asyncio`

---

## 👥 Target Users

- Users who want to set up temporary video/audio feeds over LAN without installing heavy tools
- Developers or hackers looking for a custom, tweakable streaming solution
- Environments with strict firewalls or limited network permissions

---

## 🧱 Tech Stack

| Purpose          | Technology           |
|------------------|----------------------|
| Language         | Python 3.10+         |
| Video Capture    | `opencv-python`      |
| Audio Capture    | `sounddevice` or `pyaudio` |
| Networking       | Python `socket` (TCP) |
| GUI              | `PyQt5` or `Dear PyGui` |
| Threading        | `threading` or `asyncio` |
| Packaging        | `PyInstaller`        |

---

## 📆 Milestones

| Date       | Milestone                                | Status |
|------------|------------------------------------------|--------|
| 2024-06-01 | Basic server/client communication         | ⬜️     |
| 2024-06-05 | Audio and video capture working           | ⬜️     |
| 2024-06-10 | TCP stream over port 443 established      | ⬜️     |
| 2024-06-15 | Client GUI renders video and plays audio  | ⬜️     |
| 2024-06-20 | First test between two machines (LAN)     | ⬜️     |

---

## 🧠 Notes & Ideas

- Frame encoding with `cv2.imencode('.jpg', frame)` for smaller packet sizes
- Audio buffering may require careful tuning to prevent lag/choppiness
- Consider sending control messages via a separate port or using message headers
- Eventually support UDP fallback for low-latency environments
- Option to stream audio-only or video-only

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Credits / Inspiration

- OpenCV documentation and tutorials
- Python's official socket programming guide
- OBS + NDI (as a conceptual influence for LAN streaming)
