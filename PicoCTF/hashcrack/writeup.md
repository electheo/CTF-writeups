![image](https://github.com/user-attachments/assets/4d5abc06-46ec-40b5-b3c2-07578f132c21)<h1>hashcrack</h1>

From: https://play.picoctf.org/practice/challenge/475

Author: Nana Ama Atombo-Sackey

Description: A company stored a secret message on a server which got breached due to the admin using weakly hashed passwords. Can you gain access to the secret stored within the server?

Tags: Easy, Cryptography, picoCTF 2025, browser_webshell_solvable
---

<h2>General Functionality</h2>

To interact with the instance, a netcat session `nc verbal-sleep.picoctf.net 57356` is provided to users. This opens a CLI interace which prompts the user to enter a password from a given hash. Each instance of this session uses the same hash.

![image](https://github.com/user-attachments/assets/f1a6bf64-a3de-4f00-b9b1-9b713a7ef023)
