## Board Setup
After a fresh installation with

    arduino-flasher-cli flash latest
After configuating with the Arduino App Lab, we install:

    sudo apt update
    sudo apt install mc v4l-utils vlc podman sshfs

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

and make it permanent by adding in *fstab*:

    sudo nano /etc/fsta

and append:

    UUID="<your sdcard uuid>" /mnt/sd  auto  defaults,nofail 0 0
You must actualize fstab with

    sudo systemctl daemon-reload

The sdcard should be formatted in ext4 and about the size of 64Gb.

On the sdcard create these folders:

    mkdir /mnt/sd/podman
    mkdir /mnt/sd/podman_temp_space
