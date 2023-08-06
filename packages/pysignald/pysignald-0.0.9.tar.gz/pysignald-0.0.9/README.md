pysignald
=======

[![PyPI](https://img.shields.io/pypi/v/pysignald.svg)](https://pypi.org/project/pysignald/)
[![pipeline status](https://gitlab.com/stavros/pysignald/badges/master/pipeline.svg)](https://gitlab.com/stavros/pysignald/commits/master)

pysignald is a Python client for the excellent [signald](https://git.callpipe.com/finn/signald) project, which in turn
is a command-line client for the Signal messaging service.

pysignald allows you to programmatically send and receive messages to Signal.

NOTE: Unfortunately, this library might be somewhat out of date or parts of it might not be working, as the upstream API
keeps changing, breaking compatibility. If you notice any breakage, MRs to fix it would be appreciated.


Installation
------------

You can install pysignald with pip:

```
$ pip install pysignald
```


Running
-------

Just make sure you have signald installed. Here's an example of how to use pysignald:


```python
from signald import Signal, Reaction

s = Signal("+1234567890")

# If you haven't registered/verified signald, do that first:
s.register(voice=False)
s.verify("sms code")

s.send(recipient="+1098765432", text="Hello there!")
s.send(recipient_group_id="YXNkZkFTREZhc2RmQVNERg==", text="Hello group!")

for message in s.receive_messages():
    print(message)
    s.react(message.source, Reaction("🥳", message.source, message.timestamp))
```

You can also use the chat decorator interface:

```python
from signald import Signal

s = Signal("+1234567890")

@s.chat_handler("hello there", order=10)  # This is case-insensitive.
def hello_there(message, match):
    # Returning `False` as the first argument will cause matching to continue
    # after this handler runs.
    stop = False
    reply = "Hello there!"
    return stop, reply


# Matching is case-insensitive. The `order` argument signifies when
# the handler will try to match (default is 100), and functions get sorted
# by order of declaration secondly.
@s.chat_handler("hello", order=10)
def hello(message, match):
    # This will match on "hello there" as well because of the "stop" return code in
    # the function above. Both replies will be sent.
    return "Hello!"


@s.chat_handler("wave", order=20)
def react_with_waving_hand(message, match):
    # This will only react to the received message.
    # But it would be possible to send a reply and a reaction at the same time.
    stop = True
    reply = None
    reaction = "👋"
    return stop, reply, reaction


@s.chat_handler(re.compile("my name is (.*)"))  # This is case-sensitive.
def name(message, match):
    return "Hello %s." % match.group(1)


@s.chat_handler("")
def catch_all(message, match):
    # This will only be sent if nothing else matches, because matching
    # stops by default on the first function that matches.
    return "I don't know what you said."

s.run_chat()
```

Various
-------

pysignald also supports different socket paths:

```python
s = Signal("+1234567890", socket_path="/var/some/other/socket.sock")
```

It supports TCP sockets too, if you run a proxy. For example, you can proxy signald's UNIX socket over TCP with socat:

```bash
$ socat -d -d TCP4-LISTEN:15432,fork UNIX-CONNECT:/var/run/signald/signald.sock
```

Then in pysignald:

```python
s = Signal("+1234567890", socket_path=("your.serveri.ip", 15432))
```
