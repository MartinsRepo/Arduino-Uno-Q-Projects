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

## Face Analysis with Google Mediapipe

### Step 1: We install a virtual environment

[Click the Link](https://github.com/MartinsRepo/Arduino-Uno-Q-Projects/tree/main/10.%20Tips%26Tricks/Pyenv%20Virtualenv)




  > Written with [StackEdit](https://stackedit.io/).
