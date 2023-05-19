from tkinter import *

from tkinter import filedialog
from tkinter import messagebox

from core.core import *

MY_FONT = 'Times New Roman'
MY_BACKGROUND = '#505050'

root = Tk()
root.title('Visual Novel Technical Assistant')
root.resizable(False,False)
root.config(bg=MY_BACKGROUND)

file_select_frame = Frame(root, bg=MY_BACKGROUND)
file_select_frame.config()
file_select_frame.pack()

#  Global vars
file_path = StringVar()
search_filter = StringVar()

TITLES = {
    'main': 'Select an option',
    'summary': "Summary of your novel's decisions",
    'search': 'Search between the roads',
    'decisions': "Search between your novel's decisions"
}

SEARCH_EXAMPLES = {
    'Code': 'Simple: -1-3-4-\nMultiple: -1-, -27-, -36-',
    'Ending': 'Simple: good\nMultiple: bad, neutral, other',
    'Points': 'Simple: friendship >= 5\nMultiple: friendship > 8, friendship <= 11, strength > 5\nRespect the blank spaces'
}

#  Functions


def OpenAnalyticsWindow():
    ''' The main window where the user will do the basic commands '''
    mainWindow = Toplevel()
    mainWindow.title('Analytics window')
    #mainWindow.geometry('400x300')
    #mainWindow.resizable(False, False)

    def clear_menu():
        for child in menu_side.winfo_children():
            if type(child) == Label:
                if child.cget('text') in TITLES.values():
                    child.config(text='')
                else:
                    child.destroy()
            else:
                child.destroy()


    def show_summary():
        clear_menu()
        option_select.config(text=TITLES['summary'])
        summaryLabel = Label(menu_side, text=f'Total roads: {len(all_ways)}', background=MY_BACKGROUND, font=(MY_FONT, 13, 'bold'), fg='white')
        decisionsLabel = Label(menu_side, text=f'Total decisions: {len(all_decisions)}', background=MY_BACKGROUND, font=(MY_FONT, 13, 'bold'), fg='white')
        endingsLabel = Label(menu_side, text='Endings:', background=MY_BACKGROUND, font=(MY_FONT, 13, 'bold'), fg='white')


        summaryLabel.grid(column=0, row=1, sticky='w', pady=10)
        decisionsLabel.grid(column=0, row=2, sticky='w', pady=10)
        endingsLabel.grid(column=0, row=3, sticky='w', pady=(10,5))

        # creating table headers
        ending_header = Label(menu_side, text='Ending', background=MY_BACKGROUND, font=(MY_FONT, 13, 'bold'), fg='white', borderwidth=1, relief=SOLID)
        count_header = Label(menu_side, text='  Count  ', background=MY_BACKGROUND, font=(MY_FONT, 13, 'bold'), fg='white', borderwidth=1, relief=SOLID, highlightbackground='white')
        percent_header = Label(menu_side, text='  Percent  ', background=MY_BACKGROUND, font=(MY_FONT, 13, 'bold'), fg='white', borderwidth=1, relief=SOLID, highlightbackground='white')
        index_header = Label(menu_side, text='  Index  ', background=MY_BACKGROUND, font=(MY_FONT, 13, 'bold'), fg='white', borderwidth=1, relief=SOLID, highlightbackground='white')

        ending_header.grid(column=0, row=5, sticky='ew')
        count_header.grid(column=1, row=5, sticky='ew')
        percent_header.grid(column=2, row=5, sticky='ew')
        index_header.grid(column=3, row=5, sticky='ew')


        endingsStatistics = GetEndingStatistics(endings,len(all_ways))
        # filling endings table
        i = 6
        for ending, data in endingsStatistics.items():
            ed = Label(menu_side, text=ending, background=MY_BACKGROUND, font=(MY_FONT, 13), fg='white', borderwidth=1, relief=SOLID, highlightbackground='white')
            count = Label(menu_side, text=data['count'], background=MY_BACKGROUND, font=(MY_FONT, 13), fg='white', borderwidth=1, relief=SOLID, highlightbackground='white')
            percent = Label(menu_side, text=str(int(data['percent'])) + '%', background=MY_BACKGROUND, font=(MY_FONT, 13), fg='white', borderwidth=1, relief=SOLID, highlightbackground='white')
            index = Label(menu_side, text=data['index'], background=MY_BACKGROUND, font=(MY_FONT, 13), fg='white', borderwidth=1, relief=SOLID, highlightbackground='white')

            ed.grid(column=0, row=i, sticky='ew')
            count.grid(column=1, row=i, sticky='ew')
            percent.grid(column=2, row=i, sticky='ew')
            index.grid(column=3, row=i, sticky='ew')
            i += 1
     

    def show_search_menu():
        clear_menu()
        search_filter.set('Code')
        option_select.config(text=TITLES['search'])


        def change_example():
            example_value.config(text=SEARCH_EXAMPLES[search_filter.get()])

        def do_search():
            results = GetRoadsBySearch(search_filter.get(), search_entry.get())
            decisionList.delete(0, END)
            if results is None:
                decisionList.insert(0, 'Not results found')
            else:
                for i, way in enumerate(results):
                    decisionList.insert(i, way.summary(1))

                results_found.config(text=f'Resuls found: {len(results)}')
                results_percent.config(text=f'Percent: {(len(results) * 100) / len(all_ways)}%')


        search_entry = Entry(menu_side,)
        radio_container = Frame(menu_side, bg=MY_BACKGROUND)
        labelFrame = LabelFrame(menu_side, text='Search examples', bg=MY_BACKGROUND, font=(MY_FONT, 15), fg='white')
        search_buttton = Button(menu_side, text='Search', bg=MY_BACKGROUND, font=(MY_FONT, 10), fg='white', command=do_search)
        code_filter = Radiobutton(radio_container, text='Code', value='Code', variable=search_filter, bg=MY_BACKGROUND, 
                                  activebackground=MY_BACKGROUND, selectcolor=MY_BACKGROUND, font=(MY_FONT, 12), fg='white', command=change_example)
        ending_filter = Radiobutton(radio_container, text='Ending', value='Ending', variable=search_filter, bg=MY_BACKGROUND, 
                                    activebackground=MY_BACKGROUND, selectcolor=MY_BACKGROUND, font=(MY_FONT, 12), fg='white', command=change_example)
        points_filter = Radiobutton(radio_container, text='Points', value='Points', variable=search_filter, bg=MY_BACKGROUND, 
                                    activebackground=MY_BACKGROUND, selectcolor=MY_BACKGROUND, font=(MY_FONT, 12), fg='white', command=change_example)
        example_value = Label(labelFrame, text=SEARCH_EXAMPLES[search_filter.get()], background=MY_BACKGROUND, font=(MY_FONT, 13), fg='white', justify='left')
        decisionList = Listbox(menu_side)
        results_found = Label(menu_side, text='', background=MY_BACKGROUND, font=(MY_FONT, 13), fg='white', justify='left')
        results_percent = Label(menu_side, text='', background=MY_BACKGROUND, font=(MY_FONT, 13), fg='white', justify='left')

        search_entry.bind('<Return>', lambda event: do_search())

        #for i, way in enumerate(all_ways):
            #decisionList.insert(i + 1, way.summary(1))

        search_entry.grid(column=0, row=1, sticky='ew', padx=15, columnspan=3)
        search_buttton.grid(column=3, row=1, sticky='ew')
        radio_container.grid(column=0, row=2, columnspan=99)
        code_filter.grid(column=0, row=0, sticky='ew', padx=5)
        ending_filter.grid(column=1, row=0, sticky='ew', padx=5)
        points_filter.grid(column=2, row=0, sticky='ew', padx=5)
        labelFrame.grid(column=0, row=3, pady=15, padx=30, sticky='ew', columnspan=99)
        example_value.grid(column=1, row=3, pady=10, padx=20)
        decisionList.grid(column=0, row=4, sticky='ew', columnspan=99, pady=25, padx=5)
        results_found.grid(column=0, row=5)
        results_percent.grid(column=1, row=5)

        
        
        



    left_side = Frame(mainWindow, background=MY_BACKGROUND)
    options_container = Frame(left_side, background=MY_BACKGROUND, width=100, height=500)
    left_border = Frame(left_side, bg='white', width=1)    
    right_side = Frame(mainWindow, background=MY_BACKGROUND)
    menu_side = Frame(right_side, background=MY_BACKGROUND, width=500, height=500)
    summary_select = Button(options_container, text='Summary', bg=MY_BACKGROUND, font=(MY_FONT, 10), fg='white', command=show_summary)
    search_select = Button(options_container, text='Search', bg=MY_BACKGROUND, font=(MY_FONT, 10), fg='white', command=show_search_menu)
    decisions_select = Button(options_container, text='Decisions', bg=MY_BACKGROUND, font=(MY_FONT, 10), fg='white')
    option_select = Label(menu_side, text=TITLES['main'], background=MY_BACKGROUND, font=(MY_FONT, 20), fg='white', justify='center')


    left_side.grid(column=0, row=0, sticky='nsew')
    options_container.grid(column=0, row=0, sticky='nsew', pady=5)
    right_side.grid(column=1, row=0, sticky='nsew')
    menu_side.grid(column=0, row=0, sticky='nsew', padx=20)
    left_border.grid(column=1,row=0, sticky='ns', rowspan=99)
    summary_select.grid(column=0, row=0, sticky='ew', padx=5, pady=10)
    search_select.grid(column=0, row=1, sticky='ew', padx=5, pady=10)
    decisions_select.grid(column=0, row=2, sticky='ew', padx=5, pady=10)
    option_select.grid(column=0,row=0, columnspan=99, sticky='ew', pady=(10, 15))


    options_container.grid_propagate(0)
    menu_side.grid_propagate(0)
    menu_side.columnconfigure(0, weight=1)


    for col in range(options_container.grid_size()[0]):
        options_container.columnconfigure(col, weight=1)


    

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
    
    OpenAnalyticsWindow()   
    

#  Creating widgets
title = Label(file_select_frame, text='Select your decisions file', font=(MY_FONT,20), background=MY_BACKGROUND, fg='white')
browse_button = Button(file_select_frame, text='Search decisions file', bg='#404040', fg='white', command=create_or_load_decision_tree)
browse_info = Label(file_select_frame, text='', font=(MY_FONT,20), background=MY_BACKGROUND, fg='white')



#  Styling widgets
title.grid(column=0, row=0, columnspan=20, sticky='ew', pady=(5,35), padx=10)
browse_button.grid(column=0, row=2, columnspan=20, sticky='ew', pady=(5,35), padx=10)
browse_info.grid(column=0, row=3, columnspan=20, sticky='ew', pady=(5,35), padx=10)



root.mainloop()    