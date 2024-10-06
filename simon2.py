import random
import pyttsx3
from tkinter import *
import tkinter as tk
from tkinter import ttk

global engine, x
engine = None

colors = ['red', 'blue', 'yellow', 'green']
secuence = []
userSecuence = []
life = 3
score = 0
velocityInit = 100
x = 0
incrementalMode = True
circleFill = 'black'
outline = 'silver'

def init_speech_engine():
    global engine
    engine = pyttsx3.init()
    print(f"get property rate: {engine.getProperty('rate')}")
    engine.setProperty('rate', 100)  # Inicializa con la velocidad
    print(f"get property rate: {engine.getProperty('rate')}")
    engine.setProperty('language', 'en')

def secGen(sec, color):
    sec.append(color)

def userSecGen(color):
    userSecuence.append(color)
    label4.config(text=f"User Secuence: {userSecuence}")

def soundit(txt):
    global engine
    if engine is None:
        init_speech_engine()
    print(f"get property rate: {engine.getProperty('rate')}")
    engine.say(txt)
    engine.runAndWait()

def showSequence(index=0):
    if index < len(secuence):
        # Ocultar todos los cuadrantes
        for i in range(4):
            canvas.itemconfig(quadrants[i], fill=circleFill)

        # Esperar un breve período antes de mostrar el nuevo color
        root.after(200, lambda: changeColor(secuence[index], index))
    else:
        print("Secuencia mostrada: ", secuence)

def changeColor(newColor, index):
    # Iluminar el cuadrante correspondiente
    color_index = colors.index(newColor)
    canvas.itemconfig(quadrants[color_index], fill=newColor)

    soundit(newColor)
    root.after(800, lambda: showSequence(index + 1))  # Esperar 1 segundo para mostrar el siguiente color

def updateSquareColor():
    global x, engine
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
    secGen(secuence, newColor)
    print("Update Simon Sequence")
    showSequence()

def on_button_click(color):
    userSecGen(color)

def exit():
    soundit("Good Bye!")
    root.destroy()

def main():
    global label4, canvas, root, quadrants
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    root.geometry("600x600")

    # Label Simon
    label1 = tk.Label(frm, text="Simon!", font=("Arial", 24))
    label1.grid(column=0, row=0, sticky='w')

    # Score and Life Labels
    label2 = tk.Label(frm, text=f"Score: {score}")
    label2.grid(column=0, row=1, sticky='w')
    
    label3 = tk.Label(frm, text=f"Life: {life}")
    label3.grid(column=0, row=2, sticky='w')

    # Quit Button
    button1 = tk.Button(frm, text="Quit", command=exit)
    button1.grid(column=6, row=0, sticky='e')

    # Canvas for drawing
    canvas = Canvas(frm, width=200, height=200)
    canvas.grid(column=1, row=1, columnspan=2, rowspan=2, pady=10)

    # Dibujar cuadrantes
    quadrants = []
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=0, extent=90, fill=circleFill, outline=outline))   # Rojo
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=90, extent=90, fill=circleFill, outline=outline))  # Azul
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=180, extent=90, fill=circleFill, outline=outline)) # Verde
    quadrants.append(canvas.create_arc(0, 0, 200, 200, start=270, extent=90, fill=circleFill, outline=outline)) # Amarillo

    # User Sequence Label
    label4 = tk.Label(frm, text=f"User Secuence: {userSecuence}", width=30)
    label4.grid(column=1, row=3, columnspan=2)

    # Color buttons
    button2 = tk.Button(frm, text="red", command=lambda: on_button_click("red"))
    button2.grid(column=0, row=4, padx=5, pady=5)
    
    button3 = tk.Button(frm, text="blue", command=lambda: on_button_click("blue"))
    button3.grid(column=1, row=4, padx=5, pady=5)
    
    button4 = tk.Button(frm, text="yellow", command=lambda: on_button_click("yellow"))
    button4.grid(column=2, row=4, padx=5, pady=5)
    
    button5 = tk.Button(frm, text="green", command=lambda: on_button_click("green"))
    button5.grid(column=0, row=5, padx=5, pady=5)

    button6 = tk.Button(frm, text="simon secuence", command=lambda: updateSquareColor())
    button6.grid(column=4, row=6, padx=6, pady=6)
    
    # Inicializa la secuencia
    updateSquareColor()
    
    root.mainloop()

main()
