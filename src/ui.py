import tkinter as tk
import tkinter.font as tkfont
from typing import Callable
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from pathlib import Path
import scipy.integrate._ivp as ivp

# variables globales para usar en las funciones

# rutas

assets_folder = Path(__file__).parent.parent.joinpath("assets")
iconFile = assets_folder / "python_icon.ico"

# paleta de colores
background_color="#ffffff"

text_color_dark="#000000"
text_color_light="#ffffff"

red_color="#cb4f52"
red_accent_color="#973b3d"

yellow_color="#f4b183"
yellow_accent_color="#c18c67"

gray_color="#7C7C7C"
gray_accent_color="#494949"

blue_color="#4472c4"
blue_accent_color="#325491"

# parámetros

Λ       :float = None # Λ
β       :float = None # β
δ       :float = None # δ
ρ       :float = None # ρ
μ       :float = None # μ
k       :float = None # k
r1      :float = None # r1
r2      :float = None # r2
φ       :float = None # φ
γ       :float = None # γ
d1      :float = None # d1
d2      :float = None # d2

# funciones matemáticas
# Susceptibles
def S(S:float,I:float,L:float)->float:
    return Λ-β*S*(I+δ*L)-μ*L

# Exposed
def E(S:float,E:float,I:float,L:float)->float:
    return β*(1-ρ)*S*(I+δ*L)+r2*I-(μ+k*(1-r1))*E

# Infected
def I(S:float,E:float,I:float,L:float)->float:
    return β*ρ*S*(I+δ*L)+k*(1-r1)*E+γ*L-(μ+d1+φ*(1-r2)+r2)*I
# Lost
def L(I:float,L:float)->float:
    return  φ*(1-r2)*I-(μ-d2+γ)*L

# fuentes
text_font=("Segoe UI Semibold", 12)

# implementación de métodos de solución

# Euler hacia adelante
# Euler hacia atrás
# Euler modificado
# Runge-Kutta 4
# Runge-Kutta 2
# Solve_IVP

def configurar_grafica(subpanel_grafica,window):
    fig = Figure()
    
    # testing
    t = np.arange(-10, 10, .01)
    y1=[ x**2 for x in t]
    y2=[ x**3 for x in t]
    y3=[ x**4 for x in t]
    y4=[ x**5 for x in t]
    fig.add_subplot(111).plot(t, y1, t, y2, t, y3, t, y4)

    fig.add_subplot(111).grid(True)
    canvas = FigureCanvasTkAgg(fig, master=subpanel_grafica)
    canvas.get_tk_widget().pack(anchor=tk.N, fill=tk.BOTH, expand=1)
    return


'''
    calcular un porcentaje de la pantalla

    ejemplo, si quiero calcular la mitad de la pantalla, entonces el valor del porcentaje es 50.
'''
def calculate_screen_percent_size(window,porcentaje):
    global_font = tkfont.Font(font=text_font)
    global_width=int(window.winfo_width()/global_font.measure("0"))
    size=int(global_width*(porcentaje/100))
    return size


def setup_dialog_size(window,descripcion):
    global_font = tkfont.Font(font=text_font)
    width=int(global_font.measure(descripcion))
    screen_width=window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    width = int(screen_width*0.6)
    height = int(screen_height*0.15)
    start_position_x = int((screen_width - width)/2)
    start_position_y = int((screen_height - height)/2)
    window.geometry("{}x{}+{}+{}".format(width, height, start_position_x, start_position_y))
    return width

def configurar_boton_rojo(boton: tk.Button,window):
    internal_padding=calculate_screen_percent_size(window,2)
    boton.configure(background=red_color,foreground=background_color,font=text_font,borderwidth=0,highlightthickness=0,activebackground=red_accent_color,activeforeground=background_color,pady=internal_padding)
    return

def configurar_boton_amarillo(boton: tk.Button,window):
    width=calculate_screen_percent_size(window,10)
    internal_padding=calculate_screen_percent_size(window,2)
    boton.configure(background=yellow_color,width=width,foreground=background_color,font=text_font,borderwidth=0,highlightthickness=0,activebackground=yellow_accent_color,activeforeground=background_color,pady=internal_padding)
    return

def configurar_boton_amarillo_misterio(boton: tk.Button,window):
    width=calculate_screen_percent_size(window,2)
    internal_padding=calculate_screen_percent_size(window,2)
    boton.configure(background=yellow_color,width=width,foreground=background_color,font=text_font,borderwidth=0,highlightthickness=0,activebackground=yellow_accent_color,activeforeground=background_color,pady=internal_padding)
    return

def configurar_boton_azul(boton: tk.Button,window):
    width=calculate_screen_percent_size(window,2)
    internal_padding=calculate_screen_percent_size(window,2)
    boton.configure(background=blue_color,width=width,foreground=background_color,font=text_font,borderwidth=0,highlightthickness=0,activebackground=blue_accent_color,activeforeground=background_color,pady=internal_padding)

def configurar_input_parametro(entry:tk.Entry,window):
    width=calculate_screen_percent_size(window,10)

    entry.configure(width=width,font=text_font,background=background_color,foreground=text_color_dark,highlightbackground=gray_color)
    return

def configurar_boton_gris(boton: tk.Button,window):
    width=calculate_screen_percent_size(window,20)
    internal_padding=calculate_screen_percent_size(window,2)
    boton.configure(background=gray_color,width=width,foreground=background_color,font=text_font,borderwidth=0,highlightthickness=0,activebackground=gray_accent_color,activeforeground=background_color,pady=internal_padding)
    return

def agregar_boton_cerrar_ventana(panel,window):
    width=calculate_screen_percent_size(window,10)
    close = tk.Button(panel,width=width,command = lambda: window.destroy())
    close.configure( text = "Cerrar")
    configurar_boton_rojo(close,window)
    close.pack(fill = tk.Y, side=tk.LEFT,expand=False)
    
    return

def agregar_boton_cerrar_dialogo(panel,window):
    close = tk.Button(panel,command = lambda: window.destroy())
    close.configure( text = "   Aceptar   ")
    configurar_boton_rojo(close,window)
    close.pack(fill = tk.Y,anchor=tk.SE, side=tk.RIGHT,expand=True)
    
    return


def configurar_panel_cerrar_ventana(window):
    width=calculate_screen_percent_size(window,100)
    panel = tk.Frame(window,width=width,background=background_color)
    panel.pack(anchor=tk.N, fill=tk.X)
    # boton para cerrar la ventana
    agregar_boton_cerrar_ventana(panel,window)
    return

def configurar_panel_cerrar_dialogo(window):
    width=calculate_screen_percent_size(window,100)
    panel = tk.Frame(window,width=width,background=background_color)
    panel.pack(anchor=tk.S, fill=tk.X)
    # boton para cerrar la ventana
    agregar_boton_cerrar_dialogo(panel,window)
    return

    # Euler hacia adelante

def agregar_boton_metodo(panel,window,metodo:str,funcion:Callable):
    padding=calculate_screen_percent_size(window,5)
    button = tk.Button(panel,command=funcion)
    button.configure(text=metodo)
    configurar_boton_gris(button,window)
    button.pack(anchor=tk.N,pady=padding)
    return

def create_message(parametro,descripcion):
    
    # create a toplevel window
    dialog = tk.Toplevel()
    dialog.title(parametro)
    width = setup_dialog_size(dialog,descripcion)
    dialog.resizable(width=False, height=False)
    dialog.configure(background=background_color)
    # create a label in the toplevel window
    label = tk.Label(dialog, text=descripcion,background=background_color,foreground=text_color_dark,font=text_font,wraplength=int(width*0.8))
    label.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)
    configurar_panel_cerrar_dialogo(dialog)
    dialog.grab_set()
    return

def agregar_boton_parametro(panel,window,parametro:str,descripcion:str,funcion:Callable):
    padding=calculate_screen_percent_size(window,5)
    subpanel = tk.Frame(panel,background=background_color)
    button = tk.Button(subpanel,command=funcion)
    button.configure(text=parametro)
    button_misterio = tk.Button(subpanel,command = lambda:create_message(parametro,descripcion))
    button_misterio.configure(text="?")

    configurar_boton_amarillo(button,window)
    configurar_boton_amarillo_misterio(button_misterio,window)
    button_misterio.pack(anchor=tk.N,side=tk.LEFT,pady=padding,padx=padding)
    button.pack(anchor=tk.N,side=tk.LEFT,pady=padding)
    input = tk.Entry(subpanel)
    
    input.pack(anchor=tk.CENTER,side=tk.RIGHT,pady=padding,padx=padding)
    subpanel.pack(anchor=tk.N,fill=tk.X)
    return

def configurar_panel_metodo_solucion(window):
    width = calculate_screen_percent_size(window,25)
    padding=calculate_screen_percent_size(window,5)
    panel = tk.Frame(window,width=width,background=background_color,highlightbackground=gray_color,highlightthickness=2,padx=padding)
    panel_titulo=tk.Frame(panel,width=width,background=background_color,pady=padding)
    panel_botones=tk.Frame(panel,width=width,background=background_color,padx=padding)
    
    titulo=tk.Label(panel_titulo,text="Método de solución",font=text_font,background=background_color,foreground=text_color_dark)

    dummyfunc=lambda: print("TODO: dummy function")

    botones=[   {"metodo":"Euler adelante","funcion":dummyfunc},
                {"metodo":"Euler atrás","funcion":dummyfunc},
                {"metodo":"Euler modificado","funcion":dummyfunc},
                {"metodo":"Runge-Kutta 2","funcion":dummyfunc},
                {"metodo":"Runge-Kutta 4","funcion":dummyfunc},
                {"metodo":"Solve_IVP","funcion":dummyfunc}]

    for boton in botones:
        agregar_boton_metodo(panel_botones,window,boton["metodo"],boton["funcion"])

    titulo.pack(anchor=tk.N, fill=tk.X)
    panel_titulo.pack(anchor=tk.N,fill=tk.NONE,expand=False)
    panel_botones.pack(anchor=tk.N, fill=tk.Y,expand=False)
    panel.pack(side=tk.RIGHT, fill=tk.Y,padx=padding,pady=padding)
    return

def configurar_panel_parametros(window):
    width = calculate_screen_percent_size(window,25)
    padding=calculate_screen_percent_size(window,5)
    panel = tk.Frame(window,width=width,background=background_color,highlightbackground=gray_color,highlightthickness=2,padx=padding)
    panel_titulo=tk.Frame(panel,width=width,background=background_color,pady=padding)
    panel_botones=tk.Frame(panel,width=width,background=background_color,padx=padding)
    
    titulo=tk.Label(panel_titulo,text="Parámetros",font=text_font,background=background_color,foreground=text_color_dark)

    # TODO implementar los botones
    dummyfunc=lambda: print("TODO: dummy function")

    botones=[   {"parametro":"Λ",   "funcion":dummyfunc,"descripcion":"Tasa de reclutamiento de individuos susceptibles en una comunidad."},
                {"parametro":"β",   "funcion":dummyfunc,"descripcion":"Coeficiente de transmisión."},
                {"parametro":"δ",   "funcion":dummyfunc,"descripcion":"Fracción de “pérdida de rastro” entre los infectados."},
                {"parametro":"ρ",   "funcion":dummyfunc,"descripcion":"Proporción de nuevos infectados (E) que tienen una rápida progresión a ser infecciosos (I)"},
                {"parametro":"μ",   "funcion":dummyfunc,"descripcion":"Tasa de muertes naturales"},
                {"parametro":"k",   "funcion":dummyfunc,"descripcion":"Tasa de progresión de infectados (E) a infecciosos (I)"},
                {"parametro":"r₁",  "funcion":dummyfunc,"descripcion":"Tasa de quimioprofilaxis efectiva"},
                {"parametro":"r₂",  "funcion":dummyfunc,"descripcion":"Tasa de terapias exitosas"},
                {"parametro":"φ",   "funcion":dummyfunc,"descripcion":"Tasa en que la infección deriva en “pérdida de rastro”"},
                {"parametro":"γ",   "funcion":dummyfunc,"descripcion":"Tasa en la que a quienes se les perdió el rastro retornan al hospital."},
                {"parametro":"d₁",  "funcion":dummyfunc,"descripcion":"Tasa de muerte en infecciosos"},
                {"parametro":"d₂",  "funcion":dummyfunc,"descripcion":"Tasa de muerte en “pérdida de rastro”"}]

    for boton in botones:
        agregar_boton_parametro(panel_botones,window,boton["parametro"],boton["descripcion"],boton["funcion"])

    titulo.pack(anchor=tk.N, fill=tk.X)
    panel_titulo.pack(anchor=tk.N,fill=tk.NONE,expand=False)
    panel_botones.pack(anchor=tk.N, fill=tk.Y,expand=False)
    panel.pack(side=tk.RIGHT, fill=tk.Y,padx=padding,pady=padding)
    return

def agregar_boton_importar(panel,window):
    # TODO crear funcion para importar datos
    padding=calculate_screen_percent_size(window,5)
    width=calculate_screen_percent_size(window,10)
    importar = tk.Button(panel,width= width,command = lambda: '''importar_datos()''')
    importar.configure(text = "Importar")
    configurar_boton_rojo(importar,window)
    importar.pack(side=tk.RIGHT,padx=padding)
    return

def agregar_boton_exportar(panel,window):
    padding=calculate_screen_percent_size(window,5)
    # TODO crear funcion para exportar datos
    width=calculate_screen_percent_size(window,10)

    importar = tk.Button(panel,width= width,command = lambda: '''exportar_datos()''')
    importar.configure( text = "Exportar")
    configurar_boton_rojo(importar,window)
    importar.pack(fill = tk.X, side=tk.LEFT,padx=padding)
    return

def configurar_panel_importar_exportar(panel,window):
    width = calculate_screen_percent_size(window,50)
    panel_botones=tk.Frame(panel,width=width,background=background_color,)
    agregar_boton_importar(panel_botones,window)
    agregar_boton_exportar(panel_botones,window)
    panel_botones.pack(anchor=tk.E, fill=tk.NONE)
    return

def agregar_boton_variable(panel,window,variable:str,descripcion:str,funcion:Callable):
    padding=calculate_screen_percent_size(window,5)
    subpanel = tk.Frame(panel,background=background_color,highlightbackground=gray_color,highlightthickness=2,padx=padding)
    button = tk.Button(subpanel,command=funcion)
    button.configure(text=variable)
    button_misterio = tk.Button(subpanel,command = lambda:create_message(variable,descripcion))
    button_misterio.configure(text="?")

    configurar_boton_azul(button,window)
    configurar_boton_azul(button_misterio,window)
    button.pack(side=tk.LEFT,pady=padding,padx=padding,expand=False)
    button_misterio.pack(side=tk.RIGHT,pady=padding,padx=padding,expand=False)
    subpanel.pack(side=tk.RIGHT,padx=padding,expand=False)
    return

def configurar_panel_grafica(panel,window):
    width = calculate_screen_percent_size(window,50)
    # TODO get gráfica de matplotlib

    subpanel_grafica=tk.Frame(panel,width=width,background=background_color)
    subpanel_botones=tk.Frame(panel,width=width,background=background_color)
    
    # TODO agregar botones de variables
    dummyfunc=lambda: print("TODO: dummy function")
    botones= [  {"variable":"S","funcion":dummyfunc,"descripcion":"S(t) es la cantidad de individuos susceptibles, es decir, el número de individuos en peligro de infectarse entre el total de la población."},
                {"variable":"E","funcion":dummyfunc,"descripcion":"E(t) es la cantidad de individuos infectados con la bacteria pero que no son capaces de transmitirla a otras personas."},
                {"variable":"I","funcion":dummyfunc,"descripcion":"I(t) es la cantidad de individuos infecciosos, es decir, el número de individuos infectados con síntomas que pueden transmitir la enfermedad."},
                {"variable":"L","funcion":dummyfunc,"descripcion":"L(t) es la cantidad de individuos en una población a los que se “les pierde el rastro”, son personas que comienzan a recibir terapia en el centro de salud, pero nunca regresan a los exámenes de seguimiento por diversas razones (e.g. larga duración del tratamiento, dificultad de desplazamiento, etc.). En este caso, el personal de salud puede determinar si están muertos, recuperados o no. "},
                ]

    for boton in reversed(botones):
        agregar_boton_variable(subpanel_botones,window,boton["variable"],boton["descripcion"],boton["funcion"])

    configurar_grafica(subpanel_grafica,window)

    subpanel_grafica.pack(anchor=tk.N,fill=tk.X,expand=True)
    subpanel_botones.pack(anchor=tk.CENTER,expand=True)
    return

def configurar_input_tiempo_simulacion(panel,window,campo,funcion):
    padding = calculate_screen_percent_size(window,5)
    input = tk.Entry(panel)
    input.bind("<Return>",funcion)
    input.pack(anchor=tk.CENTER,side=tk.RIGHT,pady=padding,padx=padding)
    return

def configurar_panel_tiempo_simulacion(panel,window):
    width = calculate_screen_percent_size(window,50)
    subpanel_titulo=tk.Frame(panel,width=width,background=background_color)
    subpanel_tiempo=tk.Frame(panel,width=width,background=background_color)
    
    dummyfunc=lambda: print("TODO: dummy function")

    inputs=[    {"campo":"izquierda","funcion":dummyfunc},
                {"campo":"centro","funcion":dummyfunc},
                {"campo":"derecha","funcion":dummyfunc}]
    
    for input in inputs:
        configurar_input_tiempo_simulacion(subpanel_tiempo,window,input["campo"],input["funcion"])
    titulo=tk.Label(subpanel_titulo,text="Tiempo de simulación (Años)",font=text_font,background=background_color,foreground=text_color_dark)
    titulo.pack(anchor=tk.N, fill=tk.X)
    subpanel_titulo.pack(anchor=tk.N,fill=tk.NONE,expand=False)
    subpanel_tiempo.pack(anchor=tk.N,fill=tk.NONE,expand=True)
    return

def setup_window_size(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    width = int(screen_width*0.8)
    height = int(screen_height*0.8)
    start_position_x = int((screen_width - width)/2)
    start_position_y = int((screen_height - height)/3)
    window.geometry("{}x{}+{}+{}".format(width, height, start_position_x, start_position_y))


def configurar_panel_izquierdo(window):
    width = calculate_screen_percent_size(window,50)
    padding=calculate_screen_percent_size(window,5)
    panel = tk.Frame(window,width=width,background=background_color,highlightbackground=gray_color,highlightthickness=2,padx=padding)
    panel_entrada_salida=tk.Frame(panel,width=width,background=background_color,pady=padding)
    panel_grafica=tk.Frame(panel,width=width,background=background_color,pady=padding)
    panel_tiempo_simulacion=tk.Frame(panel,width=width,background=background_color,pady=padding)
    
    configurar_panel_importar_exportar(panel_entrada_salida,window)
    configurar_panel_grafica(panel_grafica,window)
    configurar_panel_tiempo_simulacion(panel_tiempo_simulacion,window)
    panel_entrada_salida.pack(anchor=tk.N, fill=tk.X)
    panel_grafica.pack(anchor=tk.N, fill=tk.X)
    panel_tiempo_simulacion.pack(anchor=tk.N, fill=tk.X)
    panel.pack(side=tk.RIGHT, fill=tk.BOTH,expand=True,padx=padding,pady=padding)
    return


def setup_window():
    # crear instancia de la ventana
    window = tk.Tk()
    # agregar titulo a la ventana
    window.title("IBIO 2240 - Programación Científica | Proyecto final")
    '''
    asignar tamaño de la ventana
    '''
    setup_window_size(window)
    
    # restringir tamaño máximo y mínimo de la ventana
    window.resizable(False, False)
    # agregar fondo blanco a la ventana
    window.configure(background=background_color)

    # agregar icono a la ventana
    window.iconbitmap(iconFile.absolute())
    #window.iconbitmap('assets/python_icon.ico')

    '''
        Inicio de la sección de agregar botones y otros elementos de UI

    '''
    '''
        cerrar ventana

    '''
    configurar_panel_cerrar_ventana(window)
    '''
        panel "Método de solución"
    '''
    configurar_panel_metodo_solucion(window)
    '''
        panel de parámetros con inputs
    '''
    configurar_panel_parametros(window)
    
    configurar_panel_izquierdo(window)
    '''
        Graficar datos
    '''

    #configurar_panel_graficar(window)

    '''
        panel "tiempo de simulación" con inputs
    '''

    #configurar_panel_titulo_tiempo(window)

    #configurar_panel_tiempo_simulacion(window)


    # poner visible la ventana
    tk.mainloop()
    return

setup_window()
