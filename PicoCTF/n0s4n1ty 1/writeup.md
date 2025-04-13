<h1>nos4n1ty 1</h1>

From: https://play.picoctf.org/practice/challenge/482

Author: Prince Niyonshuti N.

Description: A developer has added profile picture upload functionality to a website. However, the implementation is flawed, and it presents an opportunity for you. Your mission, should you choose to accept it, is to navigate to the provided web page and locate the file upload area. Your ultimate goal is to find the hidden flag located in the /root directory.

Tags: Easy, Web Exploitation, picoCTF2025, browser_webshell_solvable
---

<h2>Initial Thoughts</h2>
Upon launching the instance, the user is prompted to upload a profile picture via the following interface on the website:
![image](https://github.com/user-attachments/assets/c9f1df2a-a2ee-4b48-893e-25a27dea6eb4)

When the picture is uploaded, a confirmation string is returned in a basic html page called /upload.php
![image](https://github.com/user-attachments/assets/48dfad7b-0c32-47dc-9c5e-fb9faa12ee4c)

The html file for the page reveals what I understand to be the image loading and previewing script:
![image](https://github.com/user-attachments/assets/c2fb1ec3-f285-469c-b738-e3c08e3457fd)

