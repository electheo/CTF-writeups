<h1> PIE TIME </h1>

From: https://play.picoctf.org/practice/challenge/490

Author: Darkraicg492

Description: Can you try to get the flag? Beware we have PIE!

Tags: Easy, Binary Explotation, PicoCTF 2025, browser_webshell_solvable
---

Initial thoughts:

The challenge is called PIE time and it is binary exploitation, therefore it is extremely likely that the position Independant Executables (PIE) are in use. https://www.redhat.com/en/blog/position-independent-executables-pie

In short,
>__"Position Independent Executables (PIE) are an output of the hardened package build process. A PIE binary and all of its dependencies are loaded into random locations within virtual memory each time the application is executed. This makes Return Oriented Programming (ROP) attacks much more difficult to execute reliably."__


