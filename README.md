# zMug.py-1.0
A Python to HTML Compiler!
![zmug logo](https://www.leonardocristiano.com/zmug/img/zmugpy_small.png)

## What is zMug exactly?

> *The Lorenz SZ40, SZ42a and SZ42b were German rotor stream cipher machines used by the German Army during World War II.*
> *...The sender then retransmitted the message but, critically, did not change the key settings from the original **"HQIBPEXEZMUG".***

zMug.py takes its name from the "Indicator", **"HQIBPEXEZMUG"**, or ZeeMug/ZedMug in the cryptography sector. Like the Indicator, zMug.py is a "decrypter": it establish a connection to a MariaDB database and then builds the HTML following the information for the selected page.

## Are there any dependencies for zMug?

Yeah, you must install [MariaDB on your machine](https://pypi.org/project/mariadb/).

## How does zMug.py v1.0 work?

zMug fetches the needed information from a MariaDB database. First of all you need to create a table for each page using the page's relative path as table name.

For example, your homepage table has to be named "/". zMug reads os.environ["REQUEST_URI"] to get the page name and then use it to fetch its information.

Each table, then, must be the following data structure:

```
tag      
  VARCHAR(x) 
  NOT NULL

parent
  VARCHAR(x)
  NOT NULL

parent_tag      
  VARCHAR(x)
  NOT NULL

id      
  VARCHAR(x)
  NOT NULL

cls
  VARCHAR(x)
att_typ
  VARCHAR(x)
att_val
  VARCHAR(x)

text 
  text*

cls, att_typ and att_val can be omitted, but you must leave them NULL (it will not throw an exception, but you'll have a blank class attribute, for example [class='']) or some whitespace as textContent (text only obv).

clean_id 
  tinyint(1)

This is a boolean, so just use 0 or 1.

x = variable max size
* = I used text, but this can be whatever you want. But, you know, this will be the tag textContent.

```
Every name is self-explanatory, and, in order to properly work, every tag must have an "id". That's because the function GetParent uses it to nest child tags into its parent.

If you don't want to render a specific tag with an id, you should put clean_id=1 for that specific tag. It will simply erase it. It's clean_id for a reason, you know.

In your directory, you now must create a .py file with just the following code:

```

#!/usr/bin/python
import zmug

zmug.start()

```

start() will call header(), and getURL(), and then it will call the MariaDB and that build() the page.

## Nice, can I see it in action?

Sure, just check my homepage (WIP as usual):

[https://www.leonardocristiano.com/](https://www.leonardocristiano.com/)

## Bah, this is riddled with bugs!

I mean, it's possible, I'm still working on it. If you find bugs, let me know! :)