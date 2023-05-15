from tkinter import *
#from tkinter.ttk import *

from tkinter import filedialog
from tkinter import messagebox

from core.core import *

MY_FONT = 'Times New Roman'
MY_BACKGROUND = '#505050'

root = Tk()
root.title('Visual Novel Technical Assistant')
root.resizable(False,False)
root.config(background=MY_BACKGROUND)

file_select_frame = Frame(root, bg=MY_BACKGROUND)
file_select_frame.config()
file_select_frame.pack()

#  Global vars
file_path = StringVar()

#  Functions
def create_or_load_decision_tree():
    file_path.set(filedialog.askopenfilename(
        initialdir='.',
        title='Select your .csv or .vnta decisions file',
        filetypes=(
            ('Decision tree', ('*.csv', '*.vnta')),
        )
    ))

    format = file_path.get()[-5:]
    
    if '.csv' in format:
        browse_info.config(text='Creating decision tree...')
    if '.vnta' in format:
        browse_info.config(text='Loading decision tree...')

    StartDecisionsTree(file_path.get())
    
    OpenMainWindow()

def OpenMainWindow():
    mainWindow = Toplevel(root)
    mainWindow.title('Analytics window')
    mainWindow.geometry('400x300')
    mainWindow.resizable(False, False)

    decisionList = Listbox(mainWindow)
    for i, way in enumerate(all_ways):
        decisionList.insert(i + 1, way)

    decisionList.grid(column=0, row=0, sticky='ew', pady=25, padx=5)
    

#  Creating widgets
title = Label(file_select_frame, text='Select your decisions file', font=(MY_FONT,20), background=MY_BACKGROUND, fg='white')
browse_button = Button(file_select_frame, text='Search decisions file', bg='#404040', fg='white', command=create_or_load_decision_tree)
browse_info = Label(file_select_frame, text='', font=(MY_FONT,20), background=MY_BACKGROUND, fg='white')



#  Styling widgets
title.grid(column=0, row=0, columnspan=20, sticky='ew', pady=(5,35), padx=10)
browse_button.grid(column=0, row=2, columnspan=20, sticky='ew', pady=(5,35), padx=10)
browse_info.grid(column=0, row=3, columnspan=20, sticky='ew', pady=(5,35), padx=10)



root.mainloop()
