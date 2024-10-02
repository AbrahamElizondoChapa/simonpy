import random
import pyttsx3
from tkinter import *
import tkinter as tk
from tkinter import ttk

colors = ['red', 'blue', 'yellow', 'green']
secuence = []
userSecuence = []
life = 3
score = 0

global engine
engine = None  # Inicializar aquí para evitar problemas al inicio

def init_speech_engine():
    global engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 250)
    engine.setProperty('language', 'es')

def secGen(sec, color):
    sec.append(color)

def userSecGen(color):
    userSecuence.append(color)
    label4.config(text=f"User Secuence: {userSecuence}")

def soundit(txt):
    if engine is None:
        init_speech_engine()  # Inicializa el motor si no está inicializado
    engine.say(txt)
    engine.runAndWait()

def showSequence(index=0):
    if index < len(secuence):
        newColor = secuence[index]
        square.config(bg=newColor)
        # Cambia el color después de 1 segundo
        soundit(newColor)
        label_square.config(text=newColor)
        root.after(50, lambda: showSequence(index + 1))

    else:
        # Aquí puedes agregar lógica para permitir al usuario ingresar la secuencia
        print("Secuencia mostrada: ", secuence)

def updateSquareColor():
    newColor = random.choice(colors)
    secGen(secuence, newColor)  # actualiza la secuencia de colores de simon
    print("Update Simon Sequence")
    showSequence()

def on_button_click(color):
    userSecGen(color)
    # Aquí puedes agregar la lógica para comparar la secuencia del usuario con la secuencia generada

def main():
    global label4, square, root, label_square
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
    button1 = tk.Button(frm, text="Quit", command=root.destroy)
    button1.grid(column=2, row=0, sticky='e')

    # Square in the center
    square = tk.Label(frm, width=20, height=10, bg='white')
    square.grid(column=1, row=1, columnspan=2, rowspan=2, pady=10)

    # Label para mostrar el color en el cuadrado
    label_square = tk.Label(square, text="", font=("Arial", 16), bg='white')
    label_square.place(relx=0.5, rely=0.5, anchor=CENTER)  # Centro del cuadrado

    # User Sequence Label
    label4 = tk.Label(frm, text=f"User Secuence: {userSecuence}", width=30)  # Ancho fijo
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
    # Inicializa el color del cuadrado
    updateSquareColor()
    
    root.mainloop()
    init_speech_engine()

main()
