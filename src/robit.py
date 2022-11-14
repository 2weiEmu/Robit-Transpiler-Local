
from tkinter import *

def main():

    window = Tk()
    window.title("Robit Transpiler (Local)")

    window.geometry("1000x500")
    
    MainFrame = Frame(window, bd=5 ,width=800, height=500)
    MainFrame.pack( side = LEFT )
    
    entry = Text(MainFrame)
    button = Button(MainFrame, text="Run Code")
    label = Label(MainFrame, text="Enter Pseudocode Here")
    entry.pack()
    label.pack()
    button.pack()
    
    
    OutputFrame = Frame(window, bd=5, width=200, height=500)
    OutputFrame.configure(background="#C5C4C4")
    OutputFrame.pack( side = RIGHT)
    
    output = Label(OutputFrame, font=("Lucida Console", 12), text="Code output will go here...")
    output.pack()

    mainloop()



if __name__ == "__main__":
    main()