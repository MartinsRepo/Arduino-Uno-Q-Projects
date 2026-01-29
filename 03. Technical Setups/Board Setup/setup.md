## Board Setup
After a fresh installation with

    arduino-flasher-cli flash latest

we install:

    sudo apt update
    sudo apt install mc ffmeg v4l-utils vlc podman sshfs

### Exchange Folder to PC
#### Edit fuse.conf on Arduino
    sudo nano /etc/fuse.conf
and uncomment *user_allow_other*
#### Create Mount Point on PC
    sudo mkdir /mnt/pc_exchange
    sudo chown -R $USER /mnt/pc_exchange
#### Bind Mount Point (if needed, once per Arduino session)
    sshfs -o allow_other martin@pop-os:/mnt/ArduinoExchange /mnt/pc_exchange


### SD Card Binding

#### Create Mount Space

    sudo mkdir /mnt/sd
    sudo chown -R $USER /mnt/sd
    sudo mount -a
and make it permanent by adding in *fstab*:

    sudo nano /etc/fstab
and append:

    UUID="<your sdcard uuid>" /mnt/sd  auto  defaults,nofail 0 0
The sdcard should be formatted in ext4 and about the size of 64Gb.
On the sdcard create these folders:

    mkdir /mnt/podman
    mkdir /mnt/podman_temp_space

### Podman Installation on the SDCard

As shown in the chapter [Running Ollama Models](https://github.com/MartinsRepo/Arduino-Uno-Q-Projects/blob/main/01.%20GenAI%20Support/01.%20Running%20Ollama%20Models/Ollama.md) we are using **Podman** shifted to an external storage sdcard.

> Written with [StackEdit](https://stackedit.io/).


> Written with [StackEdit](https://stackedit.io/).

