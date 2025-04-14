<h1>Flag Hunters</h1>

From: https://play.picoctf.org/practice/challenge/472?page=1

Author: syreal

Description: Lyrics jump from verses to the refrain kind of like a subroutine call. There's a hidden refrain this program doesn't print by default. Can you get it to print it? There might be something in it for you.

Tags: Easy, Reverse Engineering, picoCTF 2025, browser_webshell_solvable
---

<h2>General Functionality</h2>

When connecting to the program, a series of lyrics are displayed up until the point that the user is prompted to enter an input. This input is then repeated underneath some of the subsequent stanzas.
![image](https://github.com/user-attachments/assets/57caa631-29ae-470b-8ee1-7c05ff416af9)

<h2>The Source Code</h2>

The program is a python script

<details>
  <summary>
    [Python Source Code]
  </summary>

```
import re
import time


# Read in flag from file
flag = open('flag.txt', 'r').read()

secret_intro = \
'''Pico warriors rising, puzzles laid bare,
Solving each challenge with precision and flair.
With unity and skill, flags we deliver,
The ether’s ours to conquer, '''\
+ flag + '\n'


song_flag_hunters = secret_intro +\
'''

[REFRAIN]
We’re flag hunters in the ether, lighting up the grid,
No puzzle too dark, no challenge too hid.
With every exploit we trigger, every byte we decrypt,
We’re chasing that victory, and we’ll never quit.
CROWD (Singalong here!);
RETURN

[VERSE1]
Command line wizards, we’re starting it right,
Spawning shells in the terminal, hacking all night.
Scripts and searches, grep through the void,
Every keystroke, we're a cypher's envoy.
Brute force the lock or craft that regex,
Flag on the horizon, what challenge is next?

REFRAIN;

Echoes in memory, packets in trace,
Digging through the remnants to uncover with haste.
Hex and headers, carving out clues,
Resurrect the hidden, it's forensics we choose.
Disk dumps and packet dumps, follow the trail,
Buried deep in the noise, but we will prevail.

REFRAIN;

Binary sorcerers, let’s tear it apart,
Disassemble the code to reveal the dark heart.
From opcode to logic, tracing each line,
Emulate and break it, this key will be mine.
Debugging the maze, and I see through the deceit,
Patch it up right, and watch the lock release.

REFRAIN;

Ciphertext tumbling, breaking the spin,
Feistel or AES, we’re destined to win.
Frequency, padding, primes on the run,
Vigenère, RSA, cracking them for fun.
Shift the letters, matrices fall,
Decrypt that flag and hear the ether call.

REFRAIN;

SQL injection, XSS flow,
Map the backend out, let the database show.
Inspecting each cookie, fiddler in the fight,
Capturing requests, push the payload just right.
HTML's secrets, backdoors unlocked,
In the world wide labyrinth, we’re never lost.

REFRAIN;

Stack's overflowing, breaking the chain,
ROP gadget wizardry, ride it to fame.
Heap spray in silence, memory's plight,
Race the condition, crash it just right.
Shellcode ready, smashing the frame,
Control the instruction, flags call my name.

REFRAIN;

END;
'''

MAX_LINES = 100

def reader(song, startLabel):
  lip = 0
  start = 0
  refrain = 0
  refrain_return = 0
  finished = False

  # Get list of lyric lines
  song_lines = song.splitlines()
  
  # Find startLabel, refrain and refrain return
  for i in range(0, len(song_lines)):
    if song_lines[i] == startLabel:
      start = i + 1
    elif song_lines[i] == '[REFRAIN]':
      refrain = i + 1
    elif song_lines[i] == 'RETURN':
      refrain_return = i

  # Print lyrics
  line_count = 0
  lip = start
  while not finished and line_count < MAX_LINES:
    line_count += 1
    for line in song_lines[lip].split(';'):
      if line == '' and song_lines[lip] != '':
        continue
      if line == 'REFRAIN':
        song_lines[refrain_return] = 'RETURN ' + str(lip + 1)
        lip = refrain
      elif re.match(r"CROWD.*", line):
        crowd = input('Crowd: ')
        song_lines[lip] = 'Crowd: ' + crowd
        lip += 1
      elif re.match(r"RETURN [0-9]+", line):
        lip = int(line.split()[1])
      elif line == 'END':
        finished = True
      else:
        print(line, flush=True)
        time.sleep(0.5)
        lip += 1



reader(song_flag_hunters, '[VERSE1]')
```
</details>

<h2>Overview of functionality</h2>

Firstly, our desired flag and a secret intro are appended to the start of some song lyrics. Within these lyrics there are interpreted directions for the program to parse which perform the following functions:

`[REFRAIN]` Causes the the progrma to sleep for a short moment

`RETURN` Jumps the program to a line specified by an index

`VERSE 1` Defines the start of the song

`CROWD` Allows the user to add their own lyrics

`END` Defines the end of the song and exits the reader.

The core functionality of this program is defined within the `reader(song, startLabel)` function which is called with the __song lyrics__ and start label `VERSE 1` for its parameters.

Firstly, the reader splits each newline of the song into an array of strings via:
![image](https://github.com/user-attachments/assets/aa9e4239-0b24-4ead-b639-f2020ca14ea3)

Then, it looks for the start label defined during the function call, and sets `start`, `refrain` and `refrain_return` indexes for the song lyric array accourdingly.

Now we enter the main interpreting loop for the function. 
![image](https://github.com/user-attachments/assets/cc2acf83-c3b8-41dc-8607-e4104b9ff248)

A while loop is defined to run until the song either exceeds its max lines read or the state of the song is set to finished == True. 
__It is at this point that the vulnerability can be found__

<h2>The vulnerability</h2>
During each iteration of the while loop in the main function, the indexed song_lines[lip] array has the `.split` method applied to it needlessly. This means that if a songline has a ";" character within it, the for loop will iterate twice, taking each of these sets of strings as inputs for the function.

![image](https://github.com/user-attachments/assets/dddac939-bdca-4ed1-b390-2d228ba92b58)

Since for each item in this for loop, we are checking whether the start of the string has one of the defined interpreted set of characters such as `CROWD` or `RETURN` - we can look at ways in which we can contruct a line within the song which begins with this string.

Luckily, the program prompts us for an input of this nature via the CROWD tag which uses the Python input() function to take a user string and use it within the song. 
![image](https://github.com/user-attachments/assets/263a43b8-ec56-4b69-b153-a7e55aa77487)

__By sending the string `<anycharacters>;RETURN 0`__ we can trick the program into interpreting __"RETURN 0"__ as a new line, and thus fulfilling the criteria for the interpreter to jump to that line within the song. From our initial analysis we know that our flag is near the start of the song and that by returning to this address we can retrieve it from the concatenated lyrics.

![image](https://github.com/user-attachments/assets/cfab7332-5470-4ca0-9b6d-2be734933219)

`picoCTF{70637h3r_f0r3v3r_509142d4}`

Hooray!

---

Applications used during CTF:

-Kali Linux (OS)

-Mozilla Firefox (Web Browser)

-Visual Studio Code

-Python 3


Core sources of information:

Python: https://docs.python.org/3/howto/regex.html
  - Regular expressions documentation





