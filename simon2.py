import random
import pyttsx3
from tkinter import *
import tkinter as tk
from tkinter import ttk

global engine
engine = None

global usrSeq, usrColor
usrColor = None
colors = ['red', 'blue', 'yellow', 'green']
difficulty = ['easy', 'medium', 'hard', 'very hard', 'epic']
difficultyData = {
    "easy": (1000,100),
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

def setDifficulty(k):
    global velocityInit, delay
    level = k
    value = difficultyData[k]
    delay = value[0]
    speed = value[1]
    velocityInit = speed
    print(f"nivel de dificultad: {level} -> {value}")
    print(f"delay: {delay}, rate: {velocityInit}")

def init_speech_engine():
    global engine, velocityInit
    engine = pyttsx3.init()
    print(f"get property raTe: {engine.getProperty('rate')}")
    engine.setProperty('rate', velocityInit)  # Inicializa con la velocidad
    print(f"get property rate: {engine.getProperty('rate')}")
    engine.setProperty('language', 'en')

def secGen(sec, color):
    sec.append(color)

def soundit(txt):
    global engine
    if engine is None:
        init_speech_engine()
    print(f"get property ratee: {engine.getProperty('rate')}")
    engine.say(txt)
    engine.runAndWait()

def showSequence(index=0):
    global delay
    if index < len(sequence):
        # Ocultar todos los cuadrantes
        for i in range(4):
            canvas.itemconfig(quadrants[i], fill=circleFill)
        # Esperar un breve período antes de mostrar el nuevo color
        root.after(int(delay*0.5), lambda: changeColor(sequence[index], index))
    else:
        root.after(int(delay*0.3))
        # Ocultar todos los cuadrantes
        for i in range(4):
            canvas.itemconfig(quadrants[i], fill=circleFill)
        print("Secuencia mostrada: ", sequence)

def changeColor(newColor, index):
    global delay
    # Iluminar el cuadrante correspondiente
    color_index = colors.index(newColor)
    canvas.itemconfig(quadrants[color_index], fill=newColor)

    soundit(newColor)
    root.after(delay, lambda: showSequence(index + 1))  # Esperar 1 segundo para mostrar el siguiente color

def updateSequence():
    global x, engine, menuDifficulty

    for i in range(len(difficultyData)):
        menuDifficulty.entryconfig(i,state='disabled')

    if engine is None:
        init_speech_engine()
    if incrementalMode:
        x += 10  # Incrementa la velocidad
    newVel = velocityInit + x
    print(f"New velocity = {newVel}")
    engine = pyttsx3.init()
    engine.setProperty('rate', newVel)  # Actualiza la velocidad
    print(f"get property rate: {engine.getProperty('rate')}")
    newColor = random.choice(colors)
    secGen(sequence, newColor)
    print("Update Simon Sequence")
    showSequence()

def exit():
    soundit("Good Bye!")
    root.destroy()

def simon():
    global life, userIt
    if life > 0:
        updateSequence()
        userIt = 0
        usrSeq.clear()  # Limpiar la secuencia del usuario
        root.after(1000, lambda: startWaitingForInput())

def startWaitingForInput():
    global usrColor
    usrColor = None  # Reiniciar el color del usuario para esperar clics

def clickQuadrante(event, quadrant):
    global userIt, sequence, usrSeq, usrColor, life
    
    if usrColor is None:  # Solo registrar clics si estamos esperando la entrada del usuario
        usrColor = colors[quadrant]
        secGen(usrSeq, usrColor)
        print(f"secuencia usr {usrSeq}")
        print(f"secuencia simon {sequence}")

        # Verificamos si el índice es válido
        if userIt < len(sequence):
            if usrSeq[userIt] == sequence[userIt]:
                print("correcto")
                userIt += 1
                if userIt == len(sequence):  # Si el usuario ha completado la secuencia
                    print("Usuario ha completado la secuencia")
                    usrColor = None  # Espera la siguiente secuencia
                    root.after(1000, simon)  # Comienza una nueva secuencia después de un breve retardo
            else:
                print("incorrecto")
                life -= 1
                print(f"Vida restante: {life}")
                userIt = 0
                usrSeq.clear()  # Limpiar la secuencia del usuario
                if life <= 0:
                    print("Juego terminado")
                    exit()  # Termina el juego si se han acabado las vidas
        else:
            print("Se intentó acceder a un índice inválido")

        # Restablecer usrColor para permitir más clics
        usrColor = None


def main():
    global canvas, root, quadrants, menuDifficulty
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    root.geometry("450x300")
    menuBar = tk.Menu(root)
    menuDifficulty = tk.Menu(menuBar, tearoff=0)
    
    for key in difficultyData:
        print(f"cargando opcion de menu dificultad {key}")
        menuDifficulty.add_command(label=key, command=lambda key=key: setDifficulty(key))

    menuBar.add_cascade(label='Difficulty',menu=menuDifficulty)
    menuBar.add_command(label='Exit Game', command=exit)

    # Label Simon
    label1 = tk.Label(frm, text="Simon: ", font=("Arial", 24))
    label1.grid(column=0, row=0, sticky='w')

    # Score and Life Labels
    label2 = tk.Label(frm, text=f"Life: {life}", fg='red')
    label2.grid(column=1, row=0, sticky='w')

    label3 = tk.Label(frm, text=f"Score: {score}", fg='green')
    label3.grid(column=2, row=0, sticky='w')

    #start
    button6 = tk.Button(frm, text="start", command=lambda: simon())
    button6.grid(column=8, row=0, padx=6, pady=6)

    # Canvas for drawing
    canvas = Canvas(frm, width=200, height=200)
    canvas.grid(column=1, row=1, columnspan=2, rowspan=2, pady=10)

    # Dibujar cuadrantes
    quadrants = []
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=0, extent=90, fill=circleFill, outline=outline))   # Rojo
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=90, extent=90, fill=circleFill, outline=outline))  # Azul
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=180, extent=90, fill=circleFill, outline=outline)) # Amarillo
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=270, extent=90, fill=circleFill, outline=outline)) # Verde
    
    for i, quadrant in enumerate(quadrants):
        canvas.tag_bind(quadrant,"<Button-1>", lambda event, quadrant=i: clickQuadrante(event, quadrant))
    
    root.config(menu=menuBar)
    root.mainloop()

main()
