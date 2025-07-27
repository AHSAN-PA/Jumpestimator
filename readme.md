# Jump Height Estimator

A real-time jump height estimation tool built with Python, MediaPipe Pose, and Streamlit.  It captures webcam video, detects body landmarks, tracks vertical displacement of the ankle landmark, and displays peak jump height (in pixels) live in a web UI.

---

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/jump-height-estimator.git
   cd jump-height-estimator
   ```

2. **Create a virtual environment** (optional but recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   streamlit run streamlit_app.py
   ```

---

## Program Logic

1. **Capture Video**: Opens your default webcam feed using OpenCV.
2. **Pose Detection**: Uses MediaPipe Pose to detect 33 body landmarks per frame.
3. **Landmark Selection**: Extracts the pixel-level y-coordinates of left and right ankles.
4. **Baseline Calculation**: Maintains a running maximum ankle-y to represent ground level.
5. **Jump Displacement**: Computes `displacement = baseline_y - current_ankle_y` each frame, and tracks the peak value.
6. **Annotation & Display**: Draws pose landmarks and overlay text (`Jump: XX px`) on each frame, then streams to a Streamlit UI panel.

---

## Project Structure

```text
├── streamlit_app.py        # Main Streamlit application
├── jump_estimator.py       # JumpHeightEstimator and StreamlitApp classes
├── requirements.txt        # Python dependencies
├── README.md               # This documentation
└── .gitignore              # Exclude virtual env, caches, etc.
```

---

##  Requirements

- Python 3.7+
- OpenCV (`opencv-python`)
- MediaPipe
- Streamlit(Optional)

All dependencies listed in `requirements.txt`:

```
opencv-python
mediapipe
streamlit
```

---

## Usage

- **Start**: Click “Start” in the Streamlit sidebar to begin capturing and processing.
- **Stop**: Click “Stop” to end the capture and display the final peak jump value.
- **Exit**: Close the browser tab or interrupt the process in terminal.

---

##  Dockerization

You can containerize this application using Docker for easy deployment.

### Dockerfile

```dockerfile
# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . ./

# Expose Streamlit default port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose (optional)

Create a `docker-compose.yml` to manage the service:

```yaml
version: '3.8'
services:
  jump-estimator:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1
```

### Build and Run

```bash
# Build the Docker image
docker build -t jump-estimator:latest .

# Run container (standalone)
docker run -p 8501:8501 jump-estimator:latest

# Or use Docker Compose
docker-compose up --build
```

---

## Contributing

Contributions are welcome! Please:

1. Fork the repo.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

---


## Acknowledgements

- [MediaPipe Pose](https://developers.google.com/mediapipe/solutions/pose)
- [Streamlit](https://streamlit.io/)
- Example implementations and community contributions

