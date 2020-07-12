import tkinter, random, time

labelf=[]

labelm=[]

labell=[]

def equ():


    while True:
        a = random.randint(0, 5)
        b = random.randint(0, 5)
        c = random.randint(0, 5)

        for i in range(6):
            if i <= a:
                labelf[i][0].config(bg=labelf[i][1])
            else:
                labelf[i][0].config(bg='white')
            if i <= b:
                labelm[i][0].config(bg=labelm[i][1])
            else:
                labelm[i][0].config(bg='white')
            if i <= c:
                labell[i][0].config(bg=labell[i][1])
            else:
                labell[i][0].config(bg='white')
            time.sleep(0.01)

def start(win):

    labelf.append([tkinter.Label(win, bg='white', width=5, height=1), 'green'])

    labelf.append([tkinter.Label(win, bg='white', width=5, height=1), 'green'])

    labelf.append([tkinter.Label(win, bg='white', width=5, height=1), 'green'])

    labelf.append([tkinter.Label(win, bg='white', width=5, height=1), 'green'])

    labelf.append([tkinter.Label(win, bg='white', width=5, height=1), 'green'])

    labelf.append([tkinter.Label(win, bg='white', width=5, height=1), 'green'])

    labelm.append([tkinter.Label(win, bg='white', width=5, height=1), 'red'])

    labelm.append([tkinter.Label(win, bg='white', width=5, height=1), 'red'])

    labelm.append([tkinter.Label(win, bg='white', width=5, height=1), 'red'])

    labelm.append([tkinter.Label(win, bg='white', width=5, height=1), 'red'])

    labelm.append([tkinter.Label(win, bg='white', width=5, height=1), 'red'])

    labelm.append([tkinter.Label(win, bg='white', width=5, height=1), 'red'])

    labell.append([tkinter.Label(win, bg='white', width=5, height=1), 'yellow'])

    labell.append([tkinter.Label(win, bg='white', width=5, height=1), 'yellow'])

    labell.append([tkinter.Label(win, bg='white', width=5, height=1), 'yellow'])

    labell.append([tkinter.Label(win, bg='white', width=5, height=1), 'yellow'])

    labell.append([tkinter.Label(win, bg='white', width=5, height=1), 'yellow'])

    labell.append([tkinter.Label(win, bg='white', width=5, height=1), 'yellow'])

    labelf[0][0].place(x=80, y=500)

    labelf[1][0].place(x=80, y=475)

    labelf[2][0].place(x=80, y=450)

    labelf[3][0].place(x=80, y=425)

    labelf[4][0].place(x=80, y=400)

    labelf[5][0].place(x=80, y=375)

    labelm[0][0].place(x=130, y=500)

    labelm[1][0].place(x=130, y=475)

    labelm[2][0].place(x=130, y=450)

    labelm[3][0].place(x=130, y=425)

    labelm[4][0].place(x=130, y=400)

    labelm[5][0].place(x=130, y=375)

    labell[0][0].place(x=180, y=500)

    labell[1][0].place(x=180, y=475)

    labell[2][0].place(x=180, y=450)

    labell[3][0].place(x=180, y=425)

    labell[4][0].place(x=180, y=400)

    labell[5][0].place(x=180, y=375)

    equ()

def pause():
    labelf[0][1] = 'white'
    labelf[1][1] = 'white'
    labelf[2][1] = 'white'
    labelf[3][1] = 'white'
    labelf[4][1] = 'white'
    labelf[5][1] = 'white'

    labelm[0][1] = 'white'
    labelm[1][1] = 'white'
    labelm[2][1] = 'white'
    labelm[3][1] = 'white'
    labelm[4][1] = 'white'
    labelm[5][1] = 'white'

    labell[0][1] = 'white'
    labell[1][1] = 'white'
    labell[2][1] = 'white'
    labell[3][1] = 'white'
    labell[4][1] = 'white'
    labell[5][1] = 'white'

def unpause():
    labelf[0][1] = 'green'
    labelf[1][1] = 'green'
    labelf[2][1] = 'green'
    labelf[3][1] = 'green'
    labelf[4][1] = 'green'
    labelf[5][1] = 'green'

    labelm[0][1] = 'red'
    labelm[1][1] = 'red'
    labelm[2][1] = 'red'
    labelm[3][1] = 'red'
    labelm[4][1] = 'red'
    labelm[5][1] = 'red'

    labell[0][1] = 'yellow'
    labell[1][1] = 'yellow'
    labell[2][1] = 'yellow'
    labell[3][1] = 'yellow'
    labell[4][1] = 'yellow'
    labell[5][1] = 'yellow'