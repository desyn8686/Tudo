# Tudo v0.8
## A TUI/CLI To-Do list manager/editor written in Python3.
Tudo is an intuitive and efficient to-do list tool for command line heroes like yourself.

### Current Features:
1. Attractive TUI for editing lists.
2. Vim like keybinds for efficiency.
3. Reminder scheduling

### Planned features:
1. CLI interface for quick looking at lists.
3. Syncing lists with online database.
4. Shared lists with other users (local and online).
5. Interactive tudo list as tutorial.

### Dependencies
Python3.5+
Urwid - A great python TUI library
Also - To use the reminder function of Tudo you need to have a mail server running on your machine.
       I use **postfix** and **mailx** to do all my testing. Tudo functions perfectly fine without
       a server running, you just won't receive your reminders!

## HOW-TO

Tudo is still in a rough state, but usable! I use it every day to organize my life, and to organize this project. Becauese this is a project for Linux-101, I'll be walking through all the steps to getting this code running on your own machine. Let's get started!

### Installing Tudo

First thing you need to do is pull down a copy of this repo. This can be done a couple of ways, but I would reccomend installing **git** (most Linux distros come with git installed since it was created by Linus Torvalds himself).
### Check if you have git installed:
```
git --version
```
If this doesn't work, you'll need to install git:

#### On Debian systems:
```
sudo apt-get install git
```
#### On Red Hat (Fedora) systems:
```
sudo dnf install git
```
or on older versions of Fedora...
```
sudo yum install git
```

With git installed, you can now clone this repository. Move your working directory to where you would like the project folder to go, and:
```
git clone https://github.com/e-mo/Tudo.git
```
Now you have a copy of my project!

#### Dealing with dependencies
I'll start by assuming you have Python3 on your machine. Linux loves Python, and its rare to find a distro that doesn't come with some version of both Python2 and Python3. But, just in case it is an issue:

#### Check if you have Python3 installed:
```
python3 --version
```
If this doesn't work, you'll need to install Python3:

#### On Debian systems:
```
sudo apt-get install python3
```
#### On Red Hat (Fedora) systems:
```
sudo dnf install python3
```
or on older versions of Fedora...
```
sudo yum install python3
```

Now that we have Python3, we need to make sure we have Pip3!
Pip is the installer for Python packages, and it stands (recursively) for 'Pip installs packages.'
You MOST LIKELY received Pip3 with your Python3 binary, but this isn't a guarantee, so lets make sure we have it installed!

#### Check if you have Pip3 installed:
```
pip3 --version
```
If this doesn't work, you'll need to install Pip3:

#### On Debian systems:
```
sudo apt-get install python3-pip
```
#### On Red Hat (Fedora) systems:
```
sudo dnf install python3-pip
```
or on older versions of Fedora...
```
sudo yum install python3-pip
```

Now if all this has gone well, you now have Git, Python3, and Pip3 installed.
Lets get our last dependency, a Python3 library called Urwid:

```
pip3 install urwid
```
If you run into an error here, try this instead:
```
pip3 install urwid --user
```
Warning - Do NOT user sudo with Pip.
That should satisy all our dependency needs!


#### Running install script
First thing we have to do, before booting up Tudo, is to set up the folders that Tudo is going to use to store and recall your lists and reminders. Thankfully I set up a quick script for that! 
All you need to do is run this command from within the Tudo repository base folder:
```
python3 tudo-install.py
```
If you see any errors it is because a folder it tried to create already exists... which I don't anticipate to happen to any of you.


#### Starting reminder daemon
You'll see three **.py** files in the base directory of the repository.  
tudo-install.py <-- we already ran this one. It set up our folders.  
tudo-edit.py    <-- this opens the main program. We'll get to that.  
reminderd.py    <-- this is the reminder daemon script.  

If you wish to try out the reminder feature, you'll need to have the reminder daemon running in the background. A daemon is nothing other than a program (process) that runs in the background, and as we have learned this semester that are MANY daemons running on your machine that provide a wide variety of functionality for your system. This daemon is my daemon, and I lost some sleep over getting it to work properly. It is still a bit buggy!

To start up the reminder daemon in the background:
```
nohup python3 reminderd.py > daemon.log &
```

This starts the process in the background, to run with no hangups (ignore the HUP signal), and redirect all output to a file named **daemon.log**, which it will create if none exists. If you run into any errors, I'll want to see your log file, so don't delete it!

To stop the reminder daemon, you can use these commands:
```
ps -u <your username> | grep python
```
which will list all python processes running. Using the PID from that output:
```
kill <PID of reminder daemon>
```

note - Again, all of this relies on your having a mail service running on your machine! This is not overly difficult to do, and many distros come with a service already installed. If you want to test the reminder function, and you do not have a mail service running, find a quick tutorial on how to set up **postfix** and **mailx** as they are very popular and well supported. Also feel free to ask me any questions, as I had to set up my own for this project!

#### Using the Tudo Editor
This is what we came here for! This is the main editor/manager for all your future todo-lists.

To get it started, all we need to do is:
```
python3 tudo-edit.py
```

You should now see a screen that looks something like this:
![Image](/misc/empty_manager.png "A fresh start with Tudo")


Now you'll have one brand new list on the screen. The screen can only show four lists at a time,  
but the screen can also scroll to the left or right. From here, I'll leave you with a list of keybinds.  
Thank you for trying out Tudo, and if you have any questions, respond in the project forum and I can try to help you out!  

#### Keybinds

##### Insert mode
In insert mode, keystrokes are sent through to edit the selected text. Hitting <Enter> or <Esc> will return the user to
command mode.

##### Command mode
By default, the Tudo editor opens in command mode. In command mode, keystrokes are used to issue commands to the editor.

###### Navigation

**h** - Move cursor to the left on focused task or subtask.

**H** - Move focus one list to the left. 

**l** - Move cursor to the right on focused task or subtask.

**L** - Move focus one list to the right.

**k** - Move focus up to next task or subtask.

**K** - Move focused task up one place in list.

**j** - Move focus down to next task or subtask.

**J** - Move focused task down one place in list.

**q** - Exit Tudo editor. <Ctrl-c> also works.
       
###### List manipulation

**i** - Enter insert mode on focused task or subtask.

**N** - Create new list. List is initialized with the name 'untitled' and belonging to the group 'none.'

**n** - Edit list name. Cursor will move to the name of the list, which will be highlighted. Hitting <Enter> will commit the
        name change, while <Esc> will cancel changes.
       
**g** - Edit group name. Cursor will move to the name of the group, which will be highlighted. Hitting <Enter> will commit
        the group change, while <Esc> will cancel changes.
      
**t** - Create empty task. Cursor will move to new task, and editor will enter insert mode.

**T** - Create empty subtask under focused task. Cursor will move to new task, and editor will enter insert mode.

**e** - Expand or collapse subtasks under focused task. 

**E** - Expand or collapse subtasks under focused task, AND expand or collapse subtasks for all other tasks in focused list.

        Note - A task with subtasks will show a <*> character to the right of the task index. 
        
**x** - Strike a line through focused task or subtask, or remove line from focused task or subtask.

**D** - Open delete line prompt. Hitting 'y' will confirm delete, while hittin 'n' or 'esc' will cancel.

**alt-D** - Open delete list prompt. WARNING: There is currently no way to reverse a deleted list. Careful with this one.

###### Reminders

**R** - Open reminder overlay. 

The reminder menu first asks you what you are trying to set a reminder for.

Task: The currently focused task.
List: The currently focused list.
group: The currently focused group.

Standard navigation keys are used to move through these menus, and <space> or <enter> confirms an entry.
Play around with the reminder overlay. I think you'll find it to be rather intuitive. 
       

Thats it for Tudo! Hopefully you got it working, and I hope you can put it to good use!

Oh, and one final note: If you make a mistake like deleting a task, or a list, that you didn't want to delete, you can choose not to save changes at the time of exit. This is currently the only way to reverse this kind of misake.
