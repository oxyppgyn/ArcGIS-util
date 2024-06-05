"""
portalQuickDelete.py
Creator: Tanner Hammond
Date: May 31, 2024
Description: A script for quickly removing items in ArcGIS Portal.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import *
import webbrowser
import arcgis
from arcgis import GIS

#Functions
def incRow():
    global row
    row += 1
    return row - 1

def incCol():
    global col
    col += 1
    return col - 1

def on_entry_click(event):
    if entry.get() == 'ex: domain.com/portal':
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, '')  # Insert blank for user input

def on_focusout(event):
    if entry.get() == '':
        entry.insert(0, 'ex: domain.com/portal')

def hyperlink(url):
   webbrowser.open_new_tab(url)

def insertDuring(root,widget,text):
    widget.config(state=NORMAL)
    widget.insert(tk.END, text + '\n')
    widget.config(state=DISABLED)
    root.update_idletasks()

def confirmButton():
    pass
def cancelButton():
    raise Exception('Delete Cancelled')

def main():
    try:
        #Get Variables
        portal = box1.get()
        username = box2.get()
        password = box3.get()
        owner = box4.get()
        title = box5.get()
        type_ = box6.get()

        #Login
        portal = 'https://' + portal
        insertDuring(root,txt1,f'Logging in to {portal} as {username}...')

        
        gis = GIS(portal, username, password)
        txt1.insert(tk.END, f'Successfully logged in to: {portal} as {username}')
        

        #Build Query
        query = ''
        if title != '':
            query = query + 'title: ' + title
        if type_ != '':
            query = query + 'type: ' + type_
        elif type_ != '' and query != '':
            query = query + ', type: ' + type_
        if owner != '':
            query = query + 'owner: ' + owner
        elif owner != '' and query != '':
            query = query + ', owner: ' + owner
            
        #Execute
        if query == '':
            insertDuring(root,txt1,'ERROR No query specified.')
            raise Exception('No query specified.')
        else:
            idList = []
            content = gis.content.search(query=query)
            index = 0
            for  item in content:
                id = content[index].id
                idList.append(id)
                index += 1
            popup = Toplevel()
            popupTxt = tk.Text(root,height=25, width=50)
            insertDuring(popup,popupTxt,'Items to be Deleted:')
            index = 0
            for item in content:
                insertDuring(popup,popupTxt, f'{index + 1}. {content[index].title}\t{idList[index]}')
            cancelBut = ttk.Button(popup, text ='Cancel', command=cancelButton)
            confirmBut = ttk.Button(popup, text ='Confirm', command=confirmButton)
            cancelBut.grid(row =1,column=0)
            confirmBut.grid(row =1,column=1)
            #Delete
            for item in idList:
                deleteItem = gis.content.get(item)
                deleteItem.delete()

        #Print Output
        if len(content) == 0:
            insertDuring(root,txt1, 'ERROR No items found with the query provided.')
            raise Exception('No items found with the query provided.')
        else:
            insertDuring(root,txt1,'\nItems Deleted:')
            index = 0
            for item in content:
                insertDuring(root,txt1, f'{index + 1}. {content[index].title}\t{idList[index]}')

    except Exception as error:
        insertDuring(root,txt1,'\nAn Error occurred:\n' + repr(error) + '\n')
        raise Exception(error)


#tkinter
##Main Window
root = tk.Tk()
root.geometry('450x930')
root.resizable(True, True)
style = ttk.Style()
style.theme_use('vista')
root.iconbitmap("world.ico")

##Fonts
root.title('ArcGIS Portal Quick Item Delete')
headerFont = ('Microsoft YaHei UI', 18)
subheaderFont = ('Microsoft YaHei UI', 13)
bodyFont = ('Yu Gothic UI Semilight', 12)
inputFont = ('Yu Gothic UI Light', 12)

## Labels
row = 3
col = 0
ttk.Label(root, text='Portal Login:',anchor='w', width=12, font=subheaderFont).grid(row=incRow(),pady=(10,0))
ttk.Label(root, text='Portal URL', anchor='e', width=20,font=bodyFont).grid(row=incRow(),pady=(10,0),padx=(0,5))
ttk.Label(root, text='Username', anchor='e', width=20,font=bodyFont).grid(row=incRow(),padx=(0,5))
ttk.Label(root, text='Password', anchor='e', width=20,font=bodyFont).grid(row=incRow(),padx=(0,5))
ttk.Label(root, text='Query:',anchor='w', width=12,font=subheaderFont).grid(row=incRow())
ttk.Label(root, text='Owner', anchor='e', width=20,font=bodyFont).grid(row=incRow(),padx=(0,5))
ttk.Label(root, text='Title', anchor='e', width=20,font=bodyFont).grid(row=incRow(),padx=(0,5))
ttk.Label(root, text='Item Type', anchor='e', width=20,font=bodyFont).grid(row=incRow(),padx=(0,5))

##Main
row = 0
col = 1
ttk.Label(root, text='ArcGIS Portal Quick Item Delete', font=headerFont).grid(row=incRow(), column=0,columnspan=2,pady=(20,0))
ttk.Separator(root, orient='horizontal').grid(row=incRow(),column=0, columnspan=2,pady=(0,10),padx=(50,0),sticky='ew')
ttk.Label(root, text='WARNING: Any items found with the query inputted\nhere will be deleted. Be specific!',anchor='center').grid(row=incRow(),column=0, columnspan=2)
incRow() #Empty row 
box1 = ttk.Entry(root, font=inputFont,width=30)
box1.grid(row=incRow(), column=col,pady=(20,0))
box1.insert(0, 'ex: domain.com/portal')
entry = box1
box1.bind('<FocusIn>', on_entry_click)
box1.bind('<FocusOut>', on_focusout)


box2 = ttk.Entry(root, font=inputFont,width=30)
box2.grid(row=incRow(), column=col)
box3 = ttk.Entry(root, font=inputFont,width=30,show='*')
box3.grid(row=incRow(), column=col,pady=(0,10))
incRow() #Empty row 
box4 = ttk.Entry(root, font=inputFont,width=30)
box4.grid(row=incRow(), column=col,pady=(10,0))
box5 = ttk.Entry(root, font=inputFont,width=30)
box5.grid(row=incRow(), column=col)
box6 = ttk.Entry(root, font=inputFont,width=30)
box6.grid(row=incRow(), column=col)
but1 = ttk.Button(root, text='Delete Item(s)', width=40,command=main)
but1.grid(row=incRow(), column=0,columnspan=2,pady=(30,30),padx=(25,0))

ttk.Label(root, text='Output Log:').grid(row=incRow(), column=0)
txt1 = tk.Text(root,height=25, width=50)#font=('MS UI Gothic', 12, 'bold'))
txt1.insert(END,'')
txt1.grid(row=incRow(), column=0,columnspan=2,padx=(25,0))

sourceLink = ttk.Label(root, text='Source: github/oxyppgyn',font=('Yu Gothic UI Semilight', 10),cursor='hand2')
sourceLink.grid(row=incRow(),column=0, columnspan=2)
sourceLink.bind('<Button-1>', lambda e:
hyperlink('http://www.github.com/oxyppgyn'))

##Configs
style.configure('.', font=('Yu Gothic UI Semibold', 12))
txt1.config(state=DISABLED)

##Call Window
root.mainloop()
