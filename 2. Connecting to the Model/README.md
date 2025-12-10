# Connecting the Podman Container and additional Hardware

## License 
Licensed under [Apache Version 2.0](https://www.apache.org/licenses/LICENSE-2.0). This repo follows the licence terms.

## First Steps

We can ramp up our container with port mapping by:

    podman run -d \
      --name ollama \
      -p 11434:11434 \
      -v /mnt/sd/ollama_models:/root/.ollama \
      ollama ollama run qwen3:0.6b
Now the ollama model should run, booting up takes several seconds.

With posting some commands, you should get back some results. To get back some meaningful results, we should filter it. Therefor install:

    sudo apt update && sudo apt install jq
and posting

    curl -X POST http://localhost:11434/api/generate -d '{
      "model": "qwen3:0.6B",
      "prompt": "Why is the sky blue?",
      "stream": false
    }' | jq -r '.response'

*(Annotation: The stream parameter is set to false, meaning the result is displayed, if qwen3 has finished.)*

The result can be seen here:
![result](./gallery/curl.png)
As seen, the answer takes nearly about 1.5 min. So the usage of a LLM on the Arduino is not a real time application, but some non time-critical reasoning of a signal processing program flow.


## Access via Python Script
[Code Snippet ollama_client.py](./src/ollama_client.py)

### Create a Python Environment

    sudo apt install python3.13-venv
then: 

    source .venv/bin/activate
and 

    pip install requests
Then you can run the code:

    python3 src/ollama_client.py
The result should be:

![result2](./gallery/OllamaClient.png)
 
 
 ## Integrating a USB Webcam
 Here
 
> Bus 001 Device 004: ID 045e:0810 Microsoft Corp. LifeCam HD-3000

is used.
With

    v4l2-ctl --list-devices

we see the video adapters, here video2.

 ![videoadapters](./gallery/vlc_devices.png)

On the Arduino, we install the VLC part:

    sudo apt install vlc

For the first test, we can send the camera stream via UDP to the PC and show the video:
 
    cvlc -vvv v4l2:///dev/video2 \
    --v4l2-chroma MJPG \
    --v4l2-width 320 \
    --v4l2-height 256 \
    --sout '#std{access=udp,mux=ts,dst=192.168.0.228:8080}'

if necessary, we can enlarge the UDP buffer on the Arduino:

    sudo sysctl -w net.core.wmem_max=4194304 # 4MB Max Write Buffer
Then we configure VLC on the PC:

 - Open in Media: Open network stream
 - Enter the network address: udp://@:8080
 - Click Show more options
 - and set the storage parameter to 50ms

 ![vlc](./gallery/vlc.png)



> Written with [StackEdit](https://stackedit.io/).
