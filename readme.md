# SpotiScreen - WIP
<img src="Media/spotiscreen.png" alt="Logo" width="200"/>
<br>
The aims of this project are to use a Raspberry Pi and the spotify API with a RGB LED matrix to display the users currently playing spotify song.


## Current Goals
* Develop a web interface so that the system can be controlled by another device on the network.
* Display the weather, an image or other desired information on the screen when the music has been paused.
* Streamline the power delivery to reduce power delivery to 1 cable.

## Componentry
* LED Matrix: Pimorini RGB LED Matrix Panel - 32 x 32 6mm pitch.
* Raspberry Pi model B.
* Female to Female 200mm jumper wires.
* Micro USB B Male to Micro B Female Panel Mount Extension Cable - 0.3m.
* 5.5mm x 2.1mm 12v DC Power Supply Jack Socket Chassis Panel Mount 5.5x2.1 30V/5A.
* PRO ELEC  PELL0026  5V, 4A, 20W, Plug In Power Supply, 2.1mm Plug.
* Micro USB Cable.

## Operation
Currently the user must SSH to the Raspberry Pi and run the python script using the command ``` sudo python3 main.py```.
Some of my favourite results can be seen below:

Album, Artist |  Original Album Cover | Spotiscreen Display
:-------------------------:|:-------------------------:|:-------------------------:
Ignorance is Bliss, Skepta | <img src="Media\Photos\Skepta_-_Ignorance_Is_Bliss.png" alt="Logo" width="200"/>  |  <img src="Media\Photos\iib.jpg" alt="Logo" width="200"/> 

## Hardware
These photos show the hardware design of the system:
<img src="Media\Photos\Front.jpg" alt="Logo" width="200"/> | <img src="Media\Photos\Back.jpg" alt="Logo" width="200"/>
:-------------------------:|:-------------------------:
<img src="Media\Photos\Back_Open.jpg" alt="Logo" width="200"/> | 