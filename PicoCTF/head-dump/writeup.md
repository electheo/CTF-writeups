<h1>head-dump</h1>

From: https://play.picoctf.org/practice/challenge/476

Author: Prince Niyonshuti N

Description: Welcome to the challenge! In this challenge, you will explore a web application and find an endpoint that exposes a file containing a hidden flag. The application is a simple blog website where you can read articles about various topics, including an article about API Documentation. Your goal is to explore the application and find the endpoint that generates files holding the server’s memory, where a secret flag is hidden.

Tags: Easy, Web Exploitation, picoCTF 2025, browser_webshell_solvable
---

<h2>General Functionality</h2>

When first loading into the instance, you are shown what seems to be blogging website:
![image](https://github.com/user-attachments/assets/4acad71d-4b8b-417e-8612-11cf6e90e1e4)

Clicking around on the page, most links seem to redirect to the home page. Most except for the swagger /api-docs/ page:
![image](https://github.com/user-attachments/assets/90c4819e-0b46-4975-bff7-d79dc55d69ec)

I think that I would be interested in seeing an output from the `/services`, as well as the `/heapdump` apis. Trying these out with the pre-made test/execute system yields the following results:
![image](https://github.com/user-attachments/assets/52d2e3db-d829-40d7-8994-bce07239d10b)

![image](https://github.com/user-attachments/assets/5c5f90c9-f7ac-42d7-858c-3613265dde03)

<h2>Experimentation and learning</h2>

Within the output of the headdump API, there is the option to download the returned value. When viewing the file, we see that it is extremely long and cotains sections which are lists of numbers as well as sections that have a number associated with some sort of function.

Excerpt of first section of the file: 

```
"nodes":[9,1,1,0,313,0
,9,2,3,0,23,0
,9,3,5,0,1,0
,9,4,7,0,134,0
,9,5,9,0,555,0
,9,6,11,0,75,0
,9,7,13,0,0,0
,9,8,15,0,0,0
,9,9,17,0,238,0
,9,10,19,0,5,0
,9,11,21,0,0,0
,9,12,23,0,5,0
,9,13,25,0,31,0
,9,14,27,0,1567,0
,9,15,29,0,706,0
,9,16,31,0,305,0
,9,17,33,0,0,0
,9,6,35,0,3,0
```

Excerpt of later section of the file:

```
"strings":["<dummy>",
"",
"(GC roots)",
"(Internalized strings)",
"(External strings)",
"(Read-only roots)",
"(Strong roots)",
"(Smi roots)",
"(Bootstrapper)",
"(Isolate)",
"(Relocatable)",
"(Debugger)",
"(Compilation cache)",
"(Handle scope)",
"(Builtins)",
"(Global handles)",
"(Eternal handles)",
"(Thread manager)",
"(Extensions)",
"(Code flusher)",
"(Startup object cache)",
"(Read-only object cache)",
"(Weak collections)",
"(Wrapper tracing)",
"(Unknown)",
"system / Map",
"system / Oddball",
```

Experpt of later section of the file:

```
const express = require('express');\nconst heapdump = require('heapdump');\nconst fs = require('fs');\nconst path = require('path');\nconst { swaggerUi, specs } = require('./swagger');\n\nconst app = express();\napp.use(express.static('static'));\nconst port = process.env.NEWS_PORT || 3000;\n\napp.use(express.json()); \napp.set('view engine', 'ejs');\napp.use(express.static('public'));\n\n// Serve Swagger UI\napp.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));\n\n/**\n * @swagger\n * tags:\n *   - name: Free\n *     description: API endpoints for navigating the website.\n */\n\n\n/**\n * @swagger\n * /:\n *   get:\n *     tags:\n *       - Free\n *     summary: Welcome page\n *     responses:\n *       200:\n *         description: Returns a welcome message.\n */\napp.get('/', (req, res) => {\n  res.render('index', { title: 'Heapdump CTF Challenge API' });\n});\n\n/**\n * @swagger\n * /about:\n *   get:\n *     tags:\n *       - Free\n *     summary: About Us\n *     responses:\n *       200:\n *         description: Returns information about us.",
```

So what is a heap dump anyway? It seems to be exposing a lot of information which might be useful!
from: https://www.ibm.com/docs/ja/sdk-java-technology/8?topic=dumps-heap-dump

> __"Heap dumps contain a snapshot of all the live objects that are being used by a running Java™ application on the Java heap. You can obtain detailed information for each object instance, such as the address, type, class name, or size, and whether the instance has references to other objects.__

While researching, I came accross a potentially relevant CVE: https://nvd.nist.gov/vuln/detail/CVE-2019-17634
![image](https://github.com/user-attachments/assets/2c533724-251e-44d2-89d1-de563b51d90e)

I will persue this and check to see if the vulnerability is present if I don't find a simpler solution first.

From Explot DB: https://www.exploit-db.com/docs/50459, a few further useful terms are described for dealing with heap dumps:

<h4>OQL</h4>

__"Object Query Language (OQL) is a query language standard for
object-oriented databases modeled after SQL and developed by the Object
Data Management Group (ODMG). Because of its overall complexity the
complete OQL standard has not yet been fully implemented in any software."__

<h4>JWT</h4>

__"JSON Web Token is a proposed Internet standard for creating data with
optional signature and/or optional encryption whose payload holds JSON
that asserts some number of claims. The tokens are signed either using a
private secret or a public/private key."__

The article goes on to describe how secret keys can be retrieved from the heap dump, I'll try some basic searches on the file to see if anything jumps out:

...There are many instances of the word key, but nothing jumps out to me as being of use. Circling back to the premise of the challenge, I should be looking for an endpoint which can be exploited to reveal the hidden flag. Maybe after identifying the endpoint, I can find out how to access that device via the heap dump. The endpoint is __"the endpoint that generates files holding the server’s memory, where a secret flag is hidden"__. Since the heap dump is a dump of the server's memory, I might just need to find out what created this file or where I received it from in order to trace it backwards.

Running the API command again, we can see some details regarding the request, but I don't think these are necessarily useful:
![image](https://github.com/user-attachments/assets/25925664-5094-4177-a126-6ac55df57611)

Entering this URL causes the heap dump file to download immediately.


<h2> Win </h2>

Unfortunately, this isn't some flash trick or new learning. It feels more like a cheese, despite it being the main way to solve this challenge. The flag can be retrieved by either searching the head dump file or using the linux tool grep.
![image](https://github.com/user-attachments/assets/cd440bc8-241f-4ece-8799-f85c3750e2c1)

__`picoCTF{Pat!3nt_15_Th3_K3y_8635db4b}`__

<h2> What can we take away from this </h2>

- Try the simple things first. Sometimes the answer can be right in front of you and you miss it by investigating more complicated solutions
  
- Java heap dumps can reveal sensistive information about processes running on the system. In a real-world application, it might be possible to retrieve secret keys and login credentials, allowing attackers to bypass security measures on a web application. See Mohamed Elhadad's article https://elhadadx.medium.com/exploiting-an-exposed-swagger-file-to-achieve-rce-cceb4d1f8ad0 for an example of this.

---

Applications used during CTF:

-Kali Linux (OS)

-Mozilla Firefox (Web Browser)

Core sources of information:

IBM: https://www.ibm.com/docs/ja/sdk-java-technology/8?topic=dumps-heap-dump
  - Infromation regarding heap dumps
