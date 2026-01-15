<h1>Noisy Room</h1>

From: https://gym.uqcybersquad.org/challenges#noisy_room-37

Author: Theo

Description: I recorded a bunch of people in a noisy room, but unfortunately the one person I didn't mic was the one person who actually said something interesting! Can you help me out?

The secret message starts with flag. Put the rest of the message inside {} (without spaces) to obtain a flag of the form flag{...}..

Tags: Easy, Miscellaneous, UQ Cyber Squad
---

<h2>General functionality</h2>
The user is prompted to download a ZIP file which contains lossless .WAV audio files. From these files it is possible to retrieve the flag.

<h2>Understanding audio wave summing</h2>
Audio files represented digitally are a chronigical sequence of negative and positive amplitude instructions which when parsed via a speaker, generate air waves that we can hear as sound. For multiple sounds to be played simultaneously from a single speaker, these sounds need to be added together, combining the amplitudes of each source for each moment in time. The audio file titled "Track2.wav" is the sum of all source "Tracks" including the missing "Track1-002.wave" which contains the flag.

<p></p>
Since we know adding amplitudes results in the sum of these waveforms. Consider adding two waves where in some segments a positive and negative amplitude are added together. The resulting waveform will be closer to 0, meaning that the reproduced sound is quieter.

<img width="675" height="539" alt="image" src="https://github.com/user-attachments/assets/93870bbf-7a15-4e8a-9438-db59876928ee" />


<h2>Why is lossless important</h2>
The file type provided is intentionally .WAV because this allows the series of amplitude values (constituting the audio file) to be accurately stored. If .MP3 or another compressed audio format was chosen, compression artifacts would taint the signal and make it far more difficult to phase cancel components of the source signal.

<h2>What is phase cancellation?</h2>
Consider a crude waveform which is represented by the following sequence of amplitudes:

<p></p>

<b>(1, 0, -1, 0, 1, 0, -1, 0)</b>

We can take this waveform and invert it by multiplying all values by -1 and giving us the following sequence instead:

<p></p>

<b>(-1, 0, 1, 0, -1, 0, 1, 0)</b>

This invertion is known as flipping the polarity of the waveform and if we were to listen to the audio after it has been flipped (assuming it is not combining with any other sounds), we wouldn't be able to discern any difference from the original.

Notice what happens when we combine the flipped and unflipped sequences together. The resulting sequence is:

<b>(0, 0, 0, 0, 0, 0, 0, 0)</b>

...this represents complete silence.

<img width="745" height="362" alt="image" src="https://github.com/user-attachments/assets/f4653540-f4ad-4005-94eb-8bcae4bc6e35" />


<h2>Completing the challenge</h2>
To complete this challenge, audio editing software is required. The simplest free tool widely available for this task is Audacity which can be downloaded here: https://www.audacityteam.org/download/#

<p></p>

Start by downloading the required source files and extracting these access each .WAV file individually.

Import these into Audacity so that they all play at the same time.

<img width="1129" height="1035" alt="image" src="https://github.com/user-attachments/assets/1e408b7f-8060-4a03-8b51-b064e982c45c" />


Perform a polarity inversion on all of the tracks except for "Track2.wav". In Audacity, this is possible by selecting the tracks you wish to modify and going to (Effect->Special->Invert).

<img width="1166" height="884" alt="image" src="https://github.com/user-attachments/assets/b1e69537-460e-4172-b147-55d135d55f75" />


Play the audio and listen to see whether these inverted tracks are being subtracted from the summed "Track2". If successful you should be able to hear the sequence of letters for the flag.

[Optional], you may wish to export this cleaned audio file, reimport it  and then apply the Audacity effect (Pitch and Tempo->Sliding stretch) to slow down the sound and better hear the sequence.




