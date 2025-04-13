###SSTI1###

From: https://play.picoctf.org/practice/challenge/492

Author: Venax

Description: I made a cool website where you can announce whatever you want! Try it out!

Tags: Easy, Web Exploitation, PicoCTF 2025, browser_webshell_solvable
---

Beginning of challenge:

Immediately after launching the challenge instance you are directed to a website with basic html and a prominent form to announce to the site.
![image](https://github.com/user-attachments/assets/d9dd00a3-09f9-4cb6-9dd2-df17e5687f33)

After entering a string to the form, the website directs you to an announce page with your input text displayed.
![image](https://github.com/user-attachments/assets/b52c3e2b-6229-4f52-bb75-4f2cce7b377e)

Directly changing your URL to this announce page doesn't yield results:
![image](https://github.com/user-attachments/assets/e3fa69cf-67f8-43e9-a89c-89bcbc10ebdc)

After some experimentation, I wasn't able to deduce whether this something SQL exploitable, and decided to take the hint from the PicoCTF instance. This revealed the exploit for this CTF is known as server-side-template injection.

The portswigger article: https://portswigger.net/web-security/server-side-template-injection describes this explot as __"when an attacker is able to use native template syntax to inject a malicious payload into a template, which is then executed server-side."__

After futher experimentation, and now understanding that string formatting is often performed using curly brackets {}, sending the server the a set of nested curly brackets {{}} resulted in an internal server error, error 500.
![image](https://github.com/user-attachments/assets/2b0066c4-0e89-49c9-b0a3-d1c87fede2b3)

When placing any plaintext within these braces, the error dissapears and completely blank HTML page is returned when the form is executed.

Based on the error returned, it might be possible that this application is a Flask application, see: https://www.digitalocean.com/community/tutorials/how-to-handle-errors-in-a-flask-application.

To confirm server side execution ability, we sent {{7*7}} which resulted in the page showing me the numbers 49. This implies that anything we place within the double curly braces can be evaluated. 

Following along with the portswigger article, and the indentify section, we determine that this is framework is likely using Jinja
![image](https://github.com/user-attachments/assets/1a2aee31-7607-4b5e-916c-16786617ba99)
"The payload {{7*'7'}} returns 49 in Twig and 7777777 in Jinja2."











