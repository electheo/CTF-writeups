<h1>nos4n1ty 1</h1>

From: https://play.picoctf.org/practice/challenge/482

Author: Prince Niyonshuti N.

Description: A developer has added profile picture upload functionality to a website. However, the implementation is flawed, and it presents an opportunity for you. Your mission, should you choose to accept it, is to navigate to the provided web page and locate the file upload area. Your ultimate goal is to find the hidden flag located in the /root directory.

Tags: Easy, Web Exploitation, picoCTF2025, browser_webshell_solvable
---

<h2>General functionality</h2>
Upon launching the instance, the user is prompted to upload a profile picture via the following interface on the website:

![image](https://github.com/user-attachments/assets/c9f1df2a-a2ee-4b48-893e-25a27dea6eb4)

When the picture is uploaded, a confirmation string is returned in a basic html page called /upload.php

![image](https://github.com/user-attachments/assets/48dfad7b-0c32-47dc-9c5e-fb9faa12ee4c)

The html file for the page reveals what I understand to be the image loading and previewing script:

![image](https://github.com/user-attachments/assets/c2fb1ec3-f285-469c-b738-e3c08e3457fd)

<h2>Initial Thoughts</h2>

So, we know that PHP is in use by the URL after submitting the image. We also know that the name of the file uplaoded is returned to us in a confirmation page. We might be able to inject script to this system by creating a specific file name.

We will aim for remote code execution, since this may allow us to retrieve the contents of files stored in the root of the system.

From: https://www.imperva.com/learn/application-security/php-injection/
__"RCE happens when a threat actor uploads code into your website and executes it. Typically, the source of the issue is a PHP bug that accepts user input and then evaluates it as PHP code. For example, threat actors can exploit a RCE vulnerability to create a file that contains a malicious script, designed to let the actor gain access to the target website."__

<h2>Experimentation</h2>

Sending filename: `;phpinfo();`
- returns: `The file ;phpinfo(); has been uploaded Path: uploads/;phpinfo();`

Sending filenmae: `<?php eval ("echo ".$REQUEST["uploads"].";"); ?>`
- returns `The file <?php eval (%22echo %22.$REQUEST[%22uploads%22].%22;%22); ?> has been uploaded Path: uploads/`

This means that quotation marks are being replaced with "%22". This might mean that the filename we have sent is being parsed via rawurlencode() as per https://www.php.net/manual/en/function.rawurlencode.php which describes the function as:
__"Returns a string in which all non-alphanumeric characters except -_.~ have been replaced with a percent (%) sign followed by two hex digits. This is the encoding described in » RFC 3986 for protecting literal characters from being interpreted as special URL delimiters, and for protecting URLs from being mangled by transmission media with character conversions (like some email systems)."__

