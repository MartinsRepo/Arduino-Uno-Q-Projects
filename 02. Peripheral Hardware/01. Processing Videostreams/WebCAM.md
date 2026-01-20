# Integrating and Processing WebCam Videostreams

## Integrating a USB Webcam

 Here

> Bus 001 Device 004: ID 045e:0810 Microsoft Corp. LifeCam HD-3000

is used.
With

    v4l2-ctl --list-devices
we see the video adapters, here video2.

 ![videoadapters](./gallery/vlc_devices.png)

On the Arduino, we install the VLC part:

    sudo apt update
    sudo apt install ffmpeg -y
    sudo apt install vlc
    sudo apt install libglib2.0-0 -y

For the first test, we can send the camera stream via UDP to the PC and show the video:

    cvlc -vvv v4l2:///dev/video2 \
    --v4l2-chroma MJPG \
    --v4l2-width 320 \
    --v4l2-height 256 \
    --sout '#std{access=udp,mux=ts,dst=192.168.0.228:8080}'

if necessary, we can enlarge the UDP buffer on the Arduino:

    sudo sysctl -w net.core.wmem_max=4194304 # 4MB Max Write Buffer

Then we configure VLC on the PC:

 - Open in Media: *Open network stream*
 - Enter the network address: **udp://@:8080**
 - Click Show more options
 - and set the storage parameter to **50ms**

  ![vlc](./gallery/vlc.png)

## Face Landmark Streaming via MediaPipe & FFmpeg

This project demonstrates an efficient pipeline to compute Google MediaPipe Face Landmarks on a **Qualcomm-based Edge Device** (e.g., Arduino Uno R4 / Qualcomm Vision AI) and stream the results with minimal latency to a host PC via UDP.

### How it Works

The program utilizes a multi-stage pipeline designed to provide smooth performance despite limited CPU resources on the Edge device:

1.  **Capture:** OpenCV captures the video stream from the webcam (`/dev/video2`) at an optimized resolution of **320x240 pixels**.

2.  **AI Processing:** Google MediaPipe analyzes the frame. To reduce CPU load, only a specific subset of landmarks is drawn: Face Oval, Eyes, Eyebrows, and Lips.

3.  **Visualization:** By disabling the default heavy landmark markers, the person remains clearly visible behind the overlay, and drawing overhead is minimized.

4.  **Encoding:** The processed frame is passed in **BGR raw format** via a pipe to an FFmpeg subprocess.

5.  **Streaming:** FFmpeg encodes the frames using `libx264` with the `baseline` profile and `zerolatency` tuning. The result is muxed into an MPEG-TS container and sent via **UDP** to the host PC's IP address.


### Prerequisites

-   **Hardware:** Qualcomm / Arduino Edge Board with a camera mapped to `/dev/video2`.

-   **Software:** FFmpeg, Python 3.12, MediaPipe, OpenCV.

-   **Network:** Both devices must be on the same local network.

### Step 1: Installation of the Virtual Environment

[Click the Link](https://github.com/MartinsRepo/Arduino-Uno-Q-Projects/tree/main/10.%20Tips%26Tricks/Pyenv%20Virtualenv//Virtualenv.md)

and activate the environment:

    pyenv activate mpipe


### Step 2: Install mediapipe

    pip install opencv-python mediapipe

### How to Run (Edge Device)
The Phyton Code can be found here:

[mpipe.py](./source/mpipe.py)

and run the program with:

    python mpipe_test.py

### How to Receive (Host PC)

To receive the stream with minimum delay and avoid the "Timestamp conversion" errors often seen in UDP streams, it is recommended to launch **VLC Media Player** via the command line with optimized caching and jitter settings:

    vlc udp://@:8080 --network-caching=100 --clock-jitter=0 --demux=h264
 This results in a landmarks decorated face:

![face](./gallery/face.png)

### Key Technical Details

-   **Resolution:** 320x240 (Balancing AI accuracy and encoding speed).

-   **Bitrate:** Forced to 1M to prevent network congestion and UDP packet loss.

-   **GOP (Group of Pictures):** Set to `-g 10` to ensure the stream recovers quickly from network errors.


> Written with [StackEdit](https://stackedit.io/).
