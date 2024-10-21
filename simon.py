import random
import pyttsx3
from tkinter import *
import tkinter as tk
from tkinter import ttk
import threading

engine = None

# Variable global para controlar el hilo
is_running = True
speech_thread = None

usrColor = None
colors = ['red', 'blue', 'yellow', 'green']
difficulty = ['easy', 'medium', 'hard', 'very hard', 'epic']
difficultyData = {
    "easy": (1000, 100),
    "medium": (500, 150),
    "hard": (250, 250),
    "very hard": (150, 300),
    "epic": (100, 400)
}
sequence = []
usrSeq = []
userIt = 0
life = 3
score = 0
velocityInit = 200
delay = 1000
x = 0
incrementalMode = True
circleFill = 'black'
outline = 'white'

def addScore(qty):
    global score
    score += qty

def addLife(qty):
    global life
    life += qty

def setDifficulty(k):
    global velocityInit, delay
    value = difficultyData[k]
    delay = value[0]
    speed = value[1]
    velocityInit = speed

def init_speech_engine():
    global engine, velocityInit
    engine = pyttsx3.init()
    engine.setProperty('rate', velocityInit)
    engine.setProperty('language', 'en')

def secGen(sec, color):
    sec.append(color)

def soundit(txt):
    global engine, is_running, speech_thread
    if engine is None:
        init_speech_engine()

    def speak():
        global is_running
        engine.say(txt)
        engine.runAndWait()

    if not is_running:
        return

    if speech_thread is not None and speech_thread.is_alive():
        return

    speech_thread = threading.Thread(target=speak)
    speech_thread.start()

def showSequence(index=0):
    global delay
    if index < len(sequence):
        for i in range(4):
            canvas.itemconfig(quadrants[i], fill=circleFill)
        root.after(int(delay * 0.75), lambda: changeColor(sequence[index], index))
    else:
        root.after(int(delay * 0.75), lambda: hideAllQuadrants())

def hideAllQuadrants():
    for i in range(4):
        canvas.itemconfig(quadrants[i], fill=circleFill)
    root.after(int(delay * 0.5))

def changeColor(newColor, index):
    global delay
    color_index = colors.index(newColor)
    canvas.itemconfig(quadrants[color_index], fill=newColor)
    root.after(int(delay * 0.25))
    soundit(newColor)
    root.after(int(delay * 0.25))
    root.after(delay, lambda: showSequence(index + 1))

def updateSequence():
    global x, velocityInit, engine

    if engine is None:
        init_speech_engine()
    if incrementalMode:
        x += 10
    newVel = velocityInit + x
    engine = pyttsx3.init()
    engine.setProperty('rate', newVel)
    newColor = random.choice(colors)
    secGen(sequence, newColor)
    showSequence()

def stop_speech_engine():
    global engine, is_running, speech_thread
    is_running = False
    if engine is not None:
        engine.stop()
        engine = None

    if speech_thread is not None:
        speech_thread.join()

def exit():
    global is_running
    is_running = False  # Detener el hilo
    stop_speech_engine()  # Detener el motor de voz
    
    # Detener cualquier acción en curso
    if speech_thread is not None:
        speech_thread.join()  # Esperar a que el hilo de voz termine

    root.destroy()  # Cerrar la ventana


def dissableDifficulty():
    global menuDifficulty
    for i in range(len(difficultyData)):
        menuDifficulty.entryconfig(i, state='disabled')

def enableDifficulty():
    global menuDifficulty
    for i in range(len(difficultyData)):
        menuDifficulty.entryconfig(i, state='normal')

def dissableStartButton():
    global buttonStart
    buttonStart.config(state='disabled')

def enableStartButton():
    global buttonStart
    buttonStart.config(state='normal')

def updateLabels():
    global labelLife, labelScore
    labelLife.config(text=f"Life: {life}")
    labelScore.config(text=f"Score: {score}")

def simon():
    global life, userIt

    dissableDifficulty()
    dissableStartButton()
    
    if life > 0:
        updateSequence()
        userIt = 0
        usrSeq.clear()
        root.after(1000, startWaitingForInput)

def startWaitingForInput():
    global usrColor
    usrColor = None

def clickQuadrant(event, quadrant):
    global userIt, sequence, usrSeq, usrColor, life, score, labelLife, labelScore, buttonStart
    
    if usrColor is None:
        usrColor = colors[quadrant]
        secGen(usrSeq, usrColor)

        canvas.itemconfig(quadrants[quadrant], fill=usrColor)
        root.after(delay, lambda: canvas.itemconfig(quadrants[quadrant], fill=circleFill))

        if userIt < len(sequence):
            if usrSeq[userIt] == sequence[userIt]:
                userIt += 1
                addScore(10)
                updateLabels()
                if userIt == len(sequence):
                    usrColor = None
                    root.after(1000, simon)
            else:
                addLife(-1)
                addScore(-3)
                userIt = 0
                usrSeq.clear()
                updateLabels()
                if life <= 0:
                    updateLabels()
                    print("Juego terminado")
                    print("Inicializando valores para jugar de nuevo.")
                    userIt = 0
                    usrSeq.clear()
                    usrColor = None
                    sequence.clear()
                    life = 3
                    score = 0
                    updateLabels()
                    enableStartButton()
                    enableDifficulty()
        else:
            print("Se intentó acceder a un índice inválido")

        usrColor = None

def main():
    global canvas, root, quadrants, menuDifficulty, labelLife, labelScore, buttonStart
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    root.geometry("450x300")
    menuBar = tk.Menu(root)
    menuDifficulty = tk.Menu(menuBar, tearoff=0)
    
    for key in difficultyData:
        menuDifficulty.add_command(label=key, command=lambda key=key: setDifficulty(key))

    menuBar.add_cascade(label='Difficulty Level', menu=menuDifficulty)
    menuBar.add_command(label='Exit Game', command=exit)

    # Label Simon
    label1 = tk.Label(frm, text="Simon: ", font=("Arial", 24))
    label1.grid(column=0, row=0, sticky='w')

    # Score and Life Labels
    labelLife = tk.Label(frm, text=f"Life: {life}", fg='red')
    labelLife.grid(column=1, row=0, sticky='w')

    labelScore = tk.Label(frm, text=f"Score: {score}", fg='green')
    labelScore.grid(column=2, row=0, sticky='w')

    # Start button
    buttonStart = tk.Button(frm, text="Start", command=lambda: simon())
    buttonStart.grid(column=8, row=0, padx=6, pady=6)

    # Canvas for drawing
    canvas = Canvas(frm, width=200, height=200)
    canvas.grid(column=1, row=1, columnspan=2, rowspan=2, pady=10)

    # Draw quadrants
    quadrants = []
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=0, extent=90, fill=circleFill, outline=outline))   # Rojo
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=90, extent=90, fill=circleFill, outline=outline))  # Azul
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=180, extent=90, fill=circleFill, outline=outline)) # Amarillo
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=270, extent=90, fill=circleFill, outline=outline)) # Verde
    
    for i, quadrant in enumerate(quadrants):
        canvas.tag_bind(quadrant, "<Button-1>", lambda event, quadrant=i: clickQuadrant(event, quadrant))
    
    root.config(menu=menuBar)
    root.mainloop()

main()
