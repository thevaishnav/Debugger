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
