# Debugger
Simple Debugger Module for python

How to use it:
	> Create a main function which should be executed to run the program
	> Create a **Debugger** class variable.
	> Call "Debugger.run" method and pass in the main function.

This will run the main function and a Debugger dialogue will appear on the screen.
To log something to Debugger, call "Debug.Log" method. The method will return a "Chunk" variable.
To add details to the Chunk:
    Chunk.add_line(self, line: str)  method inserts "line" after a linebreak.
    Chunk.append(self, text: str)    method inserts "text" where the cursor previously was.
These detail will only show up, when you click on the particular chunk, from the list shown.
To delete details from the chunk:
    Chunk.pop_charas(self, n: int=1) method deletes last n characters.
    Chunk.pop_line(self, index=-1)   method deletes "index-th" line. if index == -1, deletes last line.
To take input from user
    Chunk.input(self, label: str="") method asks user for input,
    Note: The input field will only show up when user click on a chunk that is asking for input.
To ask user for confirmation (or hold the thread until user confirm to continue)
    Debugger.wait_for_continue(self) method will display a continue button, and hold the thread until user clicks on continue button
