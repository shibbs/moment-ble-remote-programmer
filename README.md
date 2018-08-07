# moment-ble-remote-programmer
Program for uploading firmware and verifying the radio from a Raspi to the Moment Bluetooth trigger remotes

This needs to run on a Raspberry Pi V3
The repo needs to sit at /home/pi/moment-ble

This repository is designed to be pulled into the default level of a Raspberry Pi 3 Model B V1.2 that has already been set up with the correct version of raspbian. I don't think there is anything too fancy that is needed for the Upload repos, but I do recall there being some annoying BLE setup for the scanner application. To keep things simple, this repo should be pulled from a raspi that already has the correct image running. That image is stored on Steve's computer

in order to pull down the latest and greatest from the repository open a terminal window, make sure the pi is hooked up to local internet and navigate to moment-ble/moment-ble-remote-programmer. Then run:
    git pull

In order to make this actually run on start, we need to edit the bashrc script to execute our own startup script to do this :

1 - in the pi open up a new terminal window, hit ctrl+c to quit whatever may be running
2 - type in
    sudo nano /home/pi/.bashrc
3 - Scroll to the bottom of the file that opens
4 - If there is a line that starts with "source /home/pi..." then delete it.
5 - at the end of the file type in :
    source /home/pi/moment-ble/moment-ble-remote-programmer/moment-prog-script.sh
6 - Hit ctrl+o then hit "enter" to save
7 - Hit ctrl+x to exit
8 - Everything should be good now. type in
    sudo reboot
9 - Open up the terminal and check that our script is auto-running. Try programming a unit
