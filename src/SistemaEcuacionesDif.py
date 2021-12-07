import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import scipy.integrate as inte

# Estimación de la solución del sistema de ecuaciones del modelo matemático

#       F1: dS(t)/dt = Λ-βS(I+δL)-μS

#       F2: dE(t)/dt = β(1-p)S(I+δL)+r₂I-[μ+k(1-r₁)]E

#       F3: dI(t)/dt = βpS(I+δL)+k(1-r₁)E+γL-[μ+d₁+φ(1-r₂)+r₂]I

#       F4: dL(t)/dt = φ(1-r₂)I-(μ+d₂+γ)L

# Definimos la función F1
def F1(Lam,B,Mu,D,y1,y2,y3,y4):
    return Lam-B*y1*(y3+D*y4)-Mu*y1

# Definimos la función F2
def F2(B,p,D,r2,Mu,k,r1,y1,y2,y3,y4):
    return B*(1-p)*y1*(y3+D*y4)+r2*y3-(Mu+k*(1-r1))*y2

# Definimos la función F3
def F3(B,p,D,k,r1,g,Mu,d1,Si,r2,y1,y2,y3,y4):
    return B*p*y1*(y3+D*y4)+k*(1-r1)*y2+g*y4-(Mu+d1+Si*(1-r2)+r2)*y3

# Definimos la función F4
def F4(Si,r2,Mu,d2,g,y1,y2,y3,y4):
    return Si*(1-r2)*y3-(Mu+d2+g)*y4



# Creamos una función para encontrar
# simultáneamente las raíces de las
# ecuaciones resultantes del método
# de Euler hacia atrás para Y1, Y2, Y3, Y4 y Y5
def FEulerBackRoot(yt2, y1t1, y2t1, y3t1, y4t1, Lam,B,p,D,r2,Mu,Si,k,r1,g,d1,d2,h):
    return [y1t1 + h * F1(Lam,B,Mu,D, yt2[0], yt2[1], yt2[2], yt2[3]) - yt2[0],
            y2t1 + h * F2(B,p,D,r2,Mu,k,r1, yt2[0], yt2[1], yt2[2], yt2[3]) - yt2[1],
            y3t1 + h * F3(B,p,D,k,r1,g,Mu,d1,Si,r2, yt2[0], yt2[1], yt2[2], yt2[3]) - yt2[2],
            y4t1 + h * F4(Si,r2,Mu,d2,g, yt2[0], yt2[1], yt2[2], yt2[3]) - yt2[3]]

# Creamos una función para encontrar
# simultáneamente las raíces de las
# ecuaciones resultantes del método
# de Euler modificado para Y1, Y2, Y3, Y4 y Y5
def FEulerModRoot(yt2, y1t1, y2t1, y3t1, y4t1, Lam,B,p,D,r2,Mu,Si,k,r1,g,d1,d2,h):
    return [y1t1 + (h / 2.0) * (F1(Lam,B,Mu,D, y1t1, y2t1, y3t1, y4t1) + F1(Lam,B,Mu,D, yt2[0], yt2[1], yt2[2], yt2[3])) - yt2[0],
            y2t1 + (h / 2.0) * (F2(B,p,D,r2,Mu,k,r1, y1t1, y2t1, y3t1, y4t1) + F2(B,p,D,r2,Mu,k,r1, yt2[0], yt2[1], yt2[2], yt2[3])) - yt2[1],
            y3t1 + (h / 2.0) * (F3(B,p,D,k,r1,g,Mu,d1,Si,r2, y1t1, y2t1, y3t1, y4t1) + F3(B,p,D,k,r1,g,Mu,d1,Si,r2, yt2[0], yt2[1], yt2[2], yt2[3])) - yt2[2],
            y4t1 + (h / 2.0) * (F4(Si,r2,Mu,d2,g, y1t1, y2t1, y3t1, y4t1) + F4(Si,r2,Mu,d2,g, yt2[0], yt2[1], yt2[2], yt2[3])) - yt2[3]]



# Definimos un valor para h
h = 0.01

# Definimos la condición inicial para Y1, Y2, Y3, Y4, Y5

Y20 = 1500000/7800000000
Y30 = 12500000/7800000000
Y40 = 365000000/7800000000

Y10 = 35400000/7800000000


# Creamos una función con el sistema
def FSystem(t, y, Lam,B,p,D,r2,Mu,Si,k,r1,g,d1,d2):
    return [F1(Lam,B,Mu,D, y[0], y[1], y[2], y[3]), F2(B,p,D,r2,Mu,k,r1, y[0], y[1], y[2], y[3]), F3(B,p,D,k,r1,g,Mu,d1,Si,r2, y[0], y[1], y[2], y[3]),
            F4(Si,r2,Mu,d2,g, y[0], y[1], y[2], y[3])]

#Método que resuelve el sistema de ecuaciones con Euler Forward
def calcular_Euler_For(Lam,B,p,D,r2,Mu,Si,k,r1,g,d1,d2, inicio, fin):
    # Definimos el tiempo inicial
    To = inicio
    # Definimos el tiempo final
    Tf = fin

    # Creamos un arreglo de tiempo que vaya
    # desde To hasta Tf con pasos de h
    T = np.arange(To, Tf + h, h)

    Y1EulerFor = np.zeros(len(T))
    Y2EulerFor = np.zeros(len(T))
    Y3EulerFor = np.zeros(len(T))
    Y4EulerFor = np.zeros(len(T))

    #Se inicializa el primer valor de los arreglos EulerFor
    Y1EulerFor[0] = Y10
    Y2EulerFor[0] = Y20
    Y3EulerFor[0] = Y30
    Y4EulerFor[0] = Y40

    for iter in range(1, len(T)):
        Y1EulerFor[iter] = Y1EulerFor[iter - 1] + \
                           h * F1(Lam,B,Mu,D, Y1EulerFor[iter - 1], Y2EulerFor[iter - 1], Y3EulerFor[iter - 1], Y4EulerFor[iter - 1])
        Y2EulerFor[iter] = Y2EulerFor[iter - 1] + \
                           h * F2(B,p,D,r2,Mu,k,r1, Y1EulerFor[iter - 1], Y2EulerFor[iter - 1], Y3EulerFor[iter - 1],
                                  Y4EulerFor[iter - 1])
        Y3EulerFor[iter] = Y3EulerFor[iter - 1] + \
                           h * F3(B,p,D,k,r1,g,Mu,d1,Si,r2, Y1EulerFor[iter - 1], Y2EulerFor[iter - 1], Y3EulerFor[iter - 1],
                                  Y4EulerFor[iter - 1])
        Y4EulerFor[iter] = Y4EulerFor[iter - 1] + \
                           h * F4(Si,r2,Mu,d2,g, Y1EulerFor[iter - 1], Y2EulerFor[iter - 1], Y3EulerFor[iter - 1],
                                  Y4EulerFor[iter - 1])


    return T, Y1EulerFor, Y2EulerFor, Y3EulerFor, Y4EulerFor

#Método que resuelveel sistema de ecuaciones con EuleraBack
def calcular_Euler_Back(Lam,B,p,D,r2,Mu,Si,k,r1,g,d1,d2, inicio, fin):
    # Definimos el tiempo inicial
    To = inicio
    # Definimos el tiempo final
    Tf = fin

    # Creamos un arreglo de tiempo que vaya
    # desde To hasta Tf con pasos de h
    T = np.arange(To, Tf + h, h)

    # Definimos un arreglo para ir almacenando
    # los valores estimados de Y1(t), Y2(t), Y3(t), Y4(t) y Y5(t) en cada iteración
    Y1EulerBackRoot = np.zeros(len(T))
    Y2EulerBackRoot = np.zeros(len(T))
    Y3EulerBackRoot = np.zeros(len(T))
    Y4EulerBackRoot = np.zeros(len(T))
    Y5EulerBackRoot = np.zeros(len(T))

    # Inicializamos los valores de los arreglos EulerBack
    Y1EulerBackRoot[0] = Y10
    Y2EulerBackRoot[0] = Y20
    Y3EulerBackRoot[0] = Y30
    Y4EulerBackRoot[0] = Y40

    for iter in range(1, len(T)):

        #Euler hacia atrás resolviendo el sistema de ecuaciones no lineales

        SolBack = opt.fsolve(FEulerBackRoot,
                             np.array([Y1EulerBackRoot[iter - 1],
                                       Y2EulerBackRoot[iter - 1],
                                       Y3EulerBackRoot[iter - 1],
                                       Y4EulerBackRoot[iter - 1]]),
                             (Y1EulerBackRoot[iter - 1],
                              Y2EulerBackRoot[iter - 1],
                              Y3EulerBackRoot[iter - 1],
                              Y4EulerBackRoot[iter - 1],
                              Lam,B,p,D,r2,Mu,Si,k,r1,g,d1,d2,h), xtol=10 ** -15)
        Y1EulerBackRoot[iter] = SolBack[0]
        Y2EulerBackRoot[iter] = SolBack[1]
        Y3EulerBackRoot[iter] = SolBack[2]
        Y4EulerBackRoot[iter] = SolBack[3]

    return T, Y1EulerBackRoot, Y2EulerBackRoot, Y3EulerBackRoot, Y4EulerBackRoot

#Método que resuelve el sistema de ecuaciones diferenciales con Euler Modificado
def calcular_Euler_Mod(Lam,B,p,D,r2,Mu,Si,k,r1,g,d1,d2, inicio, fin):
    # Definimos el tiempo inicial
    To = inicio
    # Definimos el tiempo final
    Tf = fin


    T = np.arange(To, Tf + h, h)

    Y1EulerModRoot = np.zeros(len(T))
    Y2EulerModRoot = np.zeros(len(T))
    Y3EulerModRoot = np.zeros(len(T))
    Y4EulerModRoot = np.zeros(len(T))

    # Se inicializan los valores de los arreglos EulerMod
    Y1EulerModRoot[0] = Y10
    Y2EulerModRoot[0] = Y20
    Y3EulerModRoot[0] = Y30
    Y4EulerModRoot[0] = Y40
    for iter in range(1, len(T)):
        # Euler modificado resolviendo el sistema de ecuaciones no-lineales
        SolMod = opt.fsolve(FEulerModRoot,
                            np.array([Y1EulerModRoot[iter - 1],
                                      Y2EulerModRoot[iter - 1],
                                      Y3EulerModRoot[iter - 1],
                                      Y4EulerModRoot[iter - 1]]),
                            (Y1EulerModRoot[iter - 1],
                             Y2EulerModRoot[iter - 1],
                             Y3EulerModRoot[iter - 1],
                             Y4EulerModRoot[iter - 1],
                             Lam, B, p, D, r2, Mu, Si, k, r1, g, d1, d2, h), xtol=10 ** -15)
        Y1EulerModRoot[iter] = SolMod[0]
        Y2EulerModRoot[iter] = SolMod[1]
        Y3EulerModRoot[iter] = SolMod[2]
        Y4EulerModRoot[iter] = SolMod[3]

    return T, Y1EulerModRoot, Y2EulerModRoot, Y3EulerModRoot, Y4EulerModRoot

#Método que resuelve el sistema de ecuaciones diferenciales por RK2
def calcular_RK2(Lam,B,p,D,r2,Mu,Si,k,r1,g,d1,d2, inicio, fin):
    # Definimos el tiempo inicial
    To = inicio
    # Definimos el tiempo final
    Tf = fin

    # Creamos un arreglo de tiempo que vaya
    # desde To hasta Tf con pasos de h
    T = np.arange(To, Tf + h, h)


    Y1RK2 = np.zeros(len(T))
    Y2RK2 = np.zeros(len(T))
    Y3RK2 = np.zeros(len(T))
    Y4RK2 = np.zeros(len(T))

    #Se inicializan los primeros valores
    Y1RK2[0] = Y10
    Y2RK2[0] = Y20
    Y3RK2[0] = Y30
    Y4RK2[0] = Y40

    for iter in range(1, len(T)):

        k11 = F1(Lam,B,Mu,D, Y1RK2[iter - 1], Y2RK2[iter - 1], Y3RK2[iter - 1], Y4RK2[iter - 1])
        k21 = F2(B,p,D,r2,Mu,k,r1, Y1RK2[iter - 1], Y2RK2[iter - 1], Y3RK2[iter - 1], Y4RK2[iter - 1])
        k31 = F3(B,p,D,k,r1,g,Mu,d1,Si,r2, Y1RK2[iter - 1], Y2RK2[iter - 1], Y3RK2[iter - 1], Y4RK2[iter - 1])
        k41 = F4(Si,r2,Mu,d2,g, Y1RK2[iter - 1], Y2RK2[iter - 1], Y3RK2[iter - 1], Y4RK2[iter - 1])

        k12 = F1(Lam,B,Mu,D, Y1RK2[iter - 1] + k11 * h, Y2RK2[iter - 1] + k21 * h, Y3RK2[iter - 1] + k31 * h,
                 Y4RK2[iter - 1] + k41 * h )
        k22 = F2(B,p,D,r2,Mu,k,r1, Y1RK2[iter - 1] + k11 * h, Y2RK2[iter - 1] + k21 * h, Y3RK2[iter - 1] + k31 * h,
                 Y4RK2[iter - 1] + k41 * h )
        k32 = F3(B,p,D,k,r1,g,Mu,d1,Si,r2, Y1RK2[iter - 1] + k11 * h, Y2RK2[iter - 1] + k21 * h, Y3RK2[iter - 1] + k31 * h,
                 Y4RK2[iter - 1] + k41 * h )
        k42 = F4(Si,r2,Mu,d2,g, Y1RK2[iter - 1] + k11 * h, Y2RK2[iter - 1] + k21 * h, Y3RK2[iter - 1] + k31 * h,
                 Y4RK2[iter - 1] + k41 * h )

        Y1RK2[iter] = Y1RK2[iter - 1] + (h / 2.0) * (k11 + k12)
        Y2RK2[iter] = Y2RK2[iter - 1] + (h / 2.0) * (k21 + k22)
        Y3RK2[iter] = Y3RK2[iter - 1] + (h / 2.0) * (k31 + k32)
        Y4RK2[iter] = Y4RK2[iter - 1] + (h / 2.0) * (k41 + k42)

    return T, Y1RK2, Y2RK2, Y3RK2, Y4RK2

def calcular_RK4(Lam,B,p,D,r2,Mu,Si,k,r1,g,d1,d2, inicio, fin):
    # Definimos el tiempo inicial
    To = inicio
    # Definimos el tiempo final
    Tf = fin

    T = np.arange(To, Tf + h, h)

    Y1RK4 = np.zeros(len(T))
    Y2RK4 = np.zeros(len(T))
    Y3RK4 = np.zeros(len(T))
    Y4RK4 = np.zeros(len(T))

    Y1RK4[0] = Y10
    Y2RK4[0] = Y20
    Y3RK4[0] = Y30
    Y4RK4[0] = Y40

    for iter in range(1, len(T)):

        k11 = F1(Lam,B,Mu,D, Y1RK4[iter - 1], Y2RK4[iter - 1], Y3RK4[iter - 1], Y4RK4[iter - 1])
        k21 = F2(B,p,D,r2,Mu,k,r1, Y1RK4[iter - 1], Y2RK4[iter - 1], Y3RK4[iter - 1], Y4RK4[iter - 1])
        k31 = F3(B,p,D,k,r1,g,Mu,d1,Si,r2, Y1RK4[iter - 1], Y2RK4[iter - 1], Y3RK4[iter - 1], Y4RK4[iter - 1])
        k41 = F4(Si,r2,Mu,d2,g, Y1RK4[iter - 1], Y2RK4[iter - 1], Y3RK4[iter - 1], Y4RK4[iter - 1])


        k12 = F1(Lam,B,Mu,D, Y1RK4[iter - 1] + 0.5 * k11 * h,
                 Y2RK4[iter - 1] + 0.5 * k21 * h, Y3RK4[iter - 1] + 0.5 * k31 * h,
                 Y4RK4[iter - 1] + 0.5 * k41 * h)
        k22 = F2(B,p,D,r2,Mu,k,r1, Y1RK4[iter - 1] + 0.5 * k11 * h,
                 Y2RK4[iter - 1] + 0.5 * k21 * h, Y3RK4[iter - 1] + 0.5 * k31 * h,
                 Y4RK4[iter - 1] + 0.5 * k41 * h)
        k32 = F3(B,p,D,k,r1,g,Mu,d1,Si,r2, Y1RK4[iter - 1] + 0.5 * k11 * h,
                 Y2RK4[iter - 1] + 0.5 * k21 * h, Y3RK4[iter - 1] + 0.5 * k31 * h,
                 Y4RK4[iter - 1] + 0.5 * k41 * h)
        k42 = F4(Si,r2,Mu,d2,g, Y1RK4[iter - 1] + 0.5 * k11 * h,
                 Y2RK4[iter - 1] + 0.5 * k21 * h, Y3RK4[iter - 1] + 0.5 * k31 * h,
                 Y4RK4[iter - 1] + 0.5 * k41 * h)


        k13 = F1(Lam,B,Mu,D, Y1RK4[iter - 1] + 0.5 * k12 * h,
                 Y2RK4[iter - 1] + 0.5 * k22 * h, Y3RK4[iter - 1] + 0.5 * k32 * h,
                 Y4RK4[iter - 1] + 0.5 * k42 * h )
        k23 = F2(B,p,D,r2,Mu,k,r1, Y1RK4[iter - 1] + 0.5 * k12 * h,
                 Y2RK4[iter - 1] + 0.5 * k22 * h, Y3RK4[iter - 1] + 0.5 * k32 * h,
                 Y4RK4[iter - 1] + 0.5 * k42 * h )
        k33 = F3(B,p,D,k,r1,g,Mu,d1,Si,r2, Y1RK4[iter - 1] + 0.5 * k12 * h,
                 Y2RK4[iter - 1] + 0.5 * k22 * h, Y3RK4[iter - 1] + 0.5 * k32 * h,
                 Y4RK4[iter - 1] + 0.5 * k42 * h )
        k43 = F4(Si,r2,Mu,d2,g, Y1RK4[iter - 1] + 0.5 * k12 * h,
                 Y2RK4[iter - 1] + 0.5 * k22 * h, Y3RK4[iter - 1] + 0.5 * k32 * h,
                 Y4RK4[iter - 1] + 0.5 * k42 * h )


        k14 = F1(Lam,B,Mu,D, Y1RK4[iter - 1] + k13 * h,
                 Y2RK4[iter - 1] + k23 * h, Y3RK4[iter - 1] + k33 * h,
                 Y4RK4[iter - 1] + k43 * h )
        k24 = F2(B,p,D,r2,Mu,k,r1, Y1RK4[iter - 1] + k13 * h,
                 Y2RK4[iter - 1] + k23 * h, Y3RK4[iter - 1] + k33 * h,
                 Y4RK4[iter - 1] + k43 * h )
        k34 = F3(B,p,D,k,r1,g,Mu,d1,Si,r2, Y1RK4[iter - 1] + k13 * h,
                 Y2RK4[iter - 1] + k23 * h, Y3RK4[iter - 1] + k33 * h,
                 Y4RK4[iter - 1] + k43 * h )
        k44 = F4(Si,r2,Mu,d2,g, Y1RK4[iter - 1] + k13 * h,
                 Y2RK4[iter - 1] + k23 * h, Y3RK4[iter - 1] + k33 * h,
                 Y4RK4[iter - 1] + k43 * h )


        Y1RK4[iter] = Y1RK4[iter - 1] + (h / 6.0) * \
                      (k11 + 2.0 * k12 + 2.0 * k13 + k14)
        Y2RK4[iter] = Y2RK4[iter - 1] + (h / 6.0) * \
                      (k21 + 2.0 * k22 + 2.0 * k23 + k24)
        Y3RK4[iter] = Y3RK4[iter - 1] + (h / 6.0) * \
                      (k31 + 2.0 * k32 + 2.0 * k33 + k34)
        Y4RK4[iter] = Y4RK4[iter - 1] + (h / 6.0) * \
                      (k41 + 2.0 * k42 + 2.0 * k43 + k44)


    return T, Y1RK4, Y2RK4, Y3RK4, Y4RK4

def calcular_RK45(Lam,B,p,D,r2,Mu,Si,k,r1,g,d1,d2, inicio, fin):
    # Definimos el tiempo inicial
    To = inicio
    # Definimos el tiempo final
    Tf = fin

    T = np.arange(To, Tf + h, h)


    SolRK45 = inte.solve_ivp(FSystem, [To, Tf], [Y10, Y20, Y30, Y40], args=(Lam,B,p,D,r2,Mu,Si,k,r1,g,d1,d2), t_eval=T,
                             method='RK45')

    return T, SolRK45



def graficar( metodo, diainic, diafinal, T, Y1, Y2, Y3, Y4):
    fig = plt.figure(figsize=(10, 4.8), dpi=100) #Se crea la figura
    arreglo=[]
    plt.plot(T, Y1, "blue")  # Se grafica la función S(t)
    arreglo.append('S(t)')
    plt.plot(T, Y2, "cyan")  # Se grafica la función E(t)
    arreglo.append('E(t)')
    plt.plot(T, Y3, "r")  # Se grafica la función I(t)
    arreglo.append('I(t)')
    plt.plot(T, Y4, "g")  # Se grafica la función R(t)
    arreglo.append('L(t)')

    #Se origaniza la forma de la gráfica
    plt.xlabel("Días", fontsize=15)
    plt.title("Estimaciones "+metodo)
    plt.legend(arreglo, fontsize=12)
    plt.xlim([diainic, diafinal])
    plt.ylim([0, 250])
    plt.grid(1)
    plt.style.use('seaborn-darkgrid')
    plt.tight_layout()
    plt.close()
    return fig
