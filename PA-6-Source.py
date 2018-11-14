import tkinter.ttk
from tkinter import *
from functools import partial

seqText = 'Enter a sequence (Ex: AABCC)'
matchText = 'Enter match (Int)'
mismatchText = 'Enter mismatch (Int)'
gapText = 'Enter gap (Int)'
allowedStrings = [seqText, matchText, mismatchText, gapText]
errorLbl = None

def main():
    window = Tk()
    window.title("Global Sequence Alignment")

    seqEntry1 = Entry(window, fg='light grey', relief=FLAT, width=26)
    seqEntry1.insert(0, seqText)
    seqEntry1.grid(row=1, column=0, pady=(10,0), padx=(10,10))
    seqEntry1.bind('<FocusIn>', partial(onFocusIn, seqEntry1))
    seqEntry1.bind('<FocusOut>', partial(onFocusOut, seqEntry1, 'S'))

    seqEntry2 = Entry(window, fg='light grey', relief=FLAT, width=26)
    seqEntry2.insert(0, seqText)
    seqEntry2.grid(row=2, column=0, pady=(5,0), padx=(10,10))
    seqEntry2.bind('<FocusIn>', partial(onFocusIn, seqEntry2))
    seqEntry2.bind('<FocusOut>', partial(onFocusOut, seqEntry2, 'S'))

    match = Entry(window, fg='light grey', relief=FLAT, width=26)
    match.insert(0, matchText)
    match.grid(row=3, column=0, pady=(5,0), padx=(10,10))
    match.bind('<FocusIn>', partial(onFocusIn, match))
    match.bind('<FocusOut>', partial(onFocusOut, match, 'M'))

    mismatch = Entry(window, fg='light grey', relief=FLAT, width=26)
    mismatch.insert(0, mismatchText)
    mismatch.grid(row=4, column=0, pady=(5,0), padx=(10,10))
    mismatch.bind('<FocusIn>', partial(onFocusIn, mismatch))
    mismatch.bind('<FocusOut>', partial(onFocusOut, mismatch, 'I'))

    gap = Entry(window, fg='light grey', relief=FLAT, width=26)
    gap.insert(0, gapText)
    gap.grid(row=5, column=0, pady=(5,0), padx=(10,10))
    gap.bind('<FocusIn>', partial(onFocusIn, gap))
    gap.bind('<FocusOut>', partial(onFocusOut, gap, 'G'))

    submitBtn = Button(window, text='Submit', cursor='hand2')
    submitBtn.config(command=partial(submit, window, seqEntry1, seqEntry2, match, mismatch, gap))
    submitBtn.grid(row=6, column=0, pady=(5,0), padx=(10,10))

    sep = ttk.Separator(window, orient=VERTICAL)
    sep.grid(row=0, column=1, rowspan=8, pady=(5,5), padx=(10,10), sticky=NS)

    window.mainloop()

def onFocusIn(entry, e):
    if entry.get() in allowedStrings:
        entry.delete(0, END)
    entry.config(fg='black')

def onFocusOut(entry, entryType, e):
    if entry.get() == '':
        if entryType == 'S':
            entry.insert(0, seqText)
        elif entryType == 'M':
            entry.insert(0, matchText)
        elif entryType == 'I':
            entry.insert(0, mismatchText)
        elif entryType == 'G':
            entry.insert(0, gapText)
            
        entry.config(fg='light grey')

def checkEntries(seqEntry1, seqEntry2, match, mismatch, gap):
    valid = True
    err = ''

    if not (seqEntry1.get().isalnum() and seqEntry2.get().isalnum()):
        valid = False
        err = 'ERROR: Sequences must be alphanumeric.'
    try:
        if int(match.get()) < 0:
            valid = False
            err = 'ERROR: Match must be an integer ≥ 0.'
        elif int(mismatch.get()) > 0:
            valid = False
            err = 'ERROR: Mismatch must be an integer ≤ 0.'
        elif int(gap.get()) > 0:
            valid = False
            err = 'ERROR: Gap must be an integer ≤ 0.'
    except:
        valid = False
        err = 'ERROR: Match, mismatch, and gap must be integers.'

    return valid, err

def displayError(window, valid, err):
    global errorLbl
    
    if errorLbl is not None:
        errorLbl.destroy()

    if valid == False:
        errVar = StringVar()
        errVar.set(err)

        errorLbl = Label(window, textvariable=errVar, fg='red', wraplength=160)
        errorLbl.grid(row=7, column=0, pady=(10,0))

class Cell:
    def __init__(self, value, pointsTo):
        self.value = value
        self.pointsTo = pointsTo

    def __repr__(self):
        return str(self.value)

def initializeMatrix(seq1, seq2, gap):
    matrix = [0] * (len(seq1) + 1)
    for i in range (0, len(matrix)):
        matrix[i] = [0] * (len(seq2) + 1)

    matrix[0][0] = Cell(0, [])

    for i in range(1, len(matrix)):
        matrix[i][0] = Cell(matrix[i-1][0].value + gap, matrix[i-1][0])
    for j in range(1, len(matrix[0])):
        matrix[0][j] = Cell(matrix[0][j-1].value + gap, matrix[0][j-1])

    return matrix
    
def submit(window, seqEntry1, seqEntry2, match, mismatch, gap):
    valid, err = checkEntries(seqEntry1, seqEntry2, match, mismatch, gap)
    displayError(window, valid, err)

    if valid == True:
        matrix = initializeMatrix(seqEntry1.get(), seqEntry2.get(), int(gap.get()))

if __name__ == '__main__':
    main()
