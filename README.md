pyKlock - a clock with a k.

A multifunction timing thingy, where some [but not necessary all] of the things are useful.

pyKlock serves as a vehicle by which I learn and tinker with programming.

Previous versions of pyKlock have existed in VB.net, Lazarus [Free Pascal] and Free Basic - and may again.

Current version of pyKlock is written in Python using different GUI frameworks

	pyKlock 0 - pygubu & pySimpleGUI - finaly settled on pySimpleGUI.  
	pyKlock 1 - CustomTkinter        - Most complete.
	pyKlock 2 - Flet.                - font dialog.
	pyKlock 3 - QT.                  - problems with frame transparency, canot be toggled programable.
	pyKlock 4 - wxPython.            - problems with frame transparency, effects all child widgets.

Note : pySimpleGUI is licensed software product, but free for hobbyist [but need to register]

    
A klock built using Python and QT6 GUI Framework.

Using python 3.14.0 and QT 6.10.1.

Note : I use the correct spelling of colour on my side of the code.  :-)

- The time can be displays as either a LED Klock or as The Famous Fuzzy Time.
- The Famous Fuzzy Time displays the time in words rounded to the nearest five minutes.
- The text time can also be displayed in a number of other formats [Binary, Roman Time, Hex Time etc.]

* The font of the time text can be selected.
* The foreground and background colours can be selected.
* The background can also be set to transparent.

The status bar includes Date, Key Status, Time Type and Idle Time.  
An info line can also be displayed showing CPU usage, RAM usage, Disc capacity and Net speed.  
Key status is the status of Caps Lock, Insert, Scroll lock and Num lock.  


To install dependencies pip install -r requirements.txt

For changes see history.txt


Kevin Scott (C) 2025 :: pyKlock3 V2026.24

