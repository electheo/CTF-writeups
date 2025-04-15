<h1>FANTASY CTF</h1>

From: https://play.picoctf.org/practice/challenge/471
Author: syreal
Description: Play this short game to get familiar with terminal applications and some of the most important rules in scope for picoCTF.

Tags: Easy, General Skills, picoCTF 2025, browser_webshell_solvable
---

<h2>General Functionality</h2>

A netcat session beings a fantasy themed dialogue which then prompts the user to take an action:
```
Options:
A) *Register multiple accounts*
B) *Share an account with a friend*
C) *Register a single, private account*
[a/b/c] >
```

![image](https://github.com/user-attachments/assets/e05a2377-eb29-4a87-9874-654e370c7107)

<h2> Win </h2>

As far as sanity challenges (challenges which provide you the general functionality for interacting with platform) go, this one was quite cute. By interacting with the session, we can eventually come to our flag in a plaintext response.

![image](https://github.com/user-attachments/assets/92e74598-eb3b-4275-a96e-2da3fd78d49f)

`picoCTF{m1113n1um_3d1710n_e41acbee}`

Hooray!

---

Applications used during CTF:

- Kali Linux (OS)

Core sources of information:

- None
