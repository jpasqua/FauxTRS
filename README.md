# FauxTRS
Repository for scripts related to the Faux TRS-80 Model

`FauxLEDs.py` is a script that randomly flashes the LEDs on the Faux TRS Model. It is launched by the runtrs.sh script so you don't need to invoke it manually.

`runtrs.sh` is a bash script that can be used to launch the trs80gp emulator and the FauxLEDs script. It will pass along any arguments you provide to trs80gp. If you kill this script (e.g. CTRL-C), it will stop both trs80gp and FauxLEDs, ensuring that the GPIO susbsystem is cleaned up properly.
