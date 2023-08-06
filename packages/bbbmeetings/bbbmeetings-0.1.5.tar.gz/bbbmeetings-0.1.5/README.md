# bbbmeetings

A Library that helps with reading information regarding Big Blue Button via the BBB-API. The goal of bbbmeetings is to make it easy to generate stats about one or more BBB-Instances.

It was a non-goal to create a full coverage of the BBB-API, for ending meetings, creating meetings, managing recordings etc.



## Installation

Via pip

```
pip install bbbmeetings
```



## Usage

First we need to create a BBB Server. To allow the connection with that server you need to know its secret, which can be found using `bbb-conf -- secret` as [mentioned here](https://docs.bigbluebutton.org/admin/bbb-conf.html#--secret). You can create a server like this:

```python
from bbbmeetings import BBBServer
server = BBBServer(host="https://bbb.example.org", secret="!#%Random!#$%Fsecret!#$%")
```

For convenience bbbmeetings offers a way of treating multiple servers as one server:

```python
from bbbmeetings import BBBServers, BBBServer

# Create a BBBServers Object from multiple BBBServer-Objects
servers = BBBServers.from_list([
        BBBServer("https://bbb1.example.org", "!#%Random!#$%Fsecret!#$%"),
        BBBServer("https://bbb2.example.org", "!#%Random!#$%Fsecret!#$%"),
        BBBServer("https://bbb3.example.org", "!#%Random!#$%Fsecret!#$%"),
        BBBServer("https://bbb4.example.org", "!#%Random!#$%Fsecret!#$%"),
        BBBServer("https://bbb5.example.org", "!#%Random!#$%Fsecret!#$%"),
    ])
```

Most methods on `BBBServer` and `BBBServers` are the same, but in the following examples I will use `servers` to showcase how this module may be used:

```python
# Get a list of meetings running on all servers and print all details about them
for meeting in servers.meetings:
    print(meeting)
```

You can also get some numbers directly (in this case I use python's formatting strings):

```python
print(f"On all servers there are {servers.people} people in {servers.n_meetings} meetings. {servers.video_active} people have their webcam on, {servers.connected_with_mic} connected with mic. There are {servers.moderators} moderators.")
```

If you want to have a list of all people in all meetings on all servers run:

```python
print(f"The names of everyone on all servers are {', '.join([a.name for a in servers.attendees])}")
```

If you just want a list with the names of Presenters you can run:

```python
presenter_names = [a.name for a in servers.attendees if a.isPresenter]
```

Or if you want to know the longest running meeting:

```python
print(f"Longest running meeting is {servers.longest_duration.name} with a duration of {servers.longest_duration.duration}")
```

