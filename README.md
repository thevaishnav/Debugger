# Debugger
![Demo of Debugger](https://user-images.githubusercontent.com/61238534/151104900-2c9c8713-85c7-4170-947d-d2b94c9dd47c.gif)  


Simple Debugger Module for python

How to use it:
  - Create a main function which should be executed to run the program  
  - Create a **Debugger** class variable.  
  - Call **Debugger.run** method and pass in the main function.  

This will run the main function and a Debugger dialogue will appear on the screen.  
To log something to Debugger, call **Debug.Log** method. The method will return a **Chunk** variable.  
To add details to the Chunk:
  - `Chunk.add_line(self, line: str)`  method inserts "line" after a linebreak.
  - `Chunk.append(self, text: str)`    method inserts "text" where the cursor previously was.
These detail will only show up, when you click on the particular chunk, from the list shown.  
To delete details from the chunk:
  - `Chunk.pop_charas(self, n: int=1)` method deletes last n characters.
  - `Chunk.pop_line(self, index=-1)`   method deletes "index-th" line. if index == -1, deletes last line.

To take input from user `Chunk.input(self, label: str="")` method asks user for input,
  __Note: The input field will only show up when user click on a chunk that is asking for input.__

To ask user for confirmation (or hold the thread until user confirm to continue) `Debugger.wait_for_continue(self)` method will display a continue button, and hold the thread until user clicks on continue button

# Code running in the GIF:
```
from Debugger import Debugger

def main_func():
    chunk1 = Debug.Log("this is msg 1")
    chunk2 = Debug.Log("Chunk 2")

    chunk1.add_line("this is Chunk 1. This one is asking for input.")
    chunk2.add_line("Nope, the Chunk 2")
    inp = chunk1.input("Your Input: ")
    chunk2.add_line("Your input in Chunk 1: " + inp)
    Debug.wait_for_continue()
    chunk1.add_line("Continued")
    chunk2.add_line("Continued")



Debug = Debugger()
Debug.run(main_func)
```
