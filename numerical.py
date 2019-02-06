import math
import matplotlib.pyplot as plt
A = 87.5
B = 0
S = 0
D = 248
wavelength = 87.5
v = 340 * 100
omega = 2 * math.pi * v / wavelength

iterating_frequency = 100

def d_a(y):
    return math.sqrt(D ** 2 + (y - (B + S) / 2) ** 2)

def d_b(y):
    return math.sqrt(D **  2 + (y + (A + S) / 2) ** 2)

def phase_shift(path_difference):
    return 2 * math.pi / wavelength * path_difference

def partial_A(t, x, y):
    return math.sin(omega * t + phase_shift(d_a(y) - math.sqrt(D ** 2 + (y + x - (B + S) / 2) ** 2)))

def partial_B(t, x, y):
    return math.sin(omega *t + phase_shift(d_b(y) - math.sqrt(D ** 2 + (y + x + (A + S) / 2) ** 2)))

def SA(t, y):
    integral = 0
    x = -1/2
    dx = 1 / iterating_frequency
    while x <= 1 / 2:
        integral += partial_A(t, x, y)
        x += dx
    integral *= dx
    return integral

def SB(t, y):
    integral = 0
    x = -1/2
    dx = 1 / iterating_frequency
    while x <= 1 / 2:
        integral += partial_B(t, x, y)
        x += dx
    integral *= dx
    return integral


def SSA(y):
    t = 0
    dt = 2 * math.pi / omega / iterating_frequency
    displacement = 0
    while t <= 2 * math.pi / omega:
        displacement += SA(t, y)
        t += dt
    displacement /= (2 * math.pi / omega) / dt
    return  A * displacement

def SSB(y):
    t = 0
    dt = 2 * math.pi / omega / iterating_frequency
    displacement = 0
    while t <= 2 * math.pi / omega:
        displacement += SB(t, y)
        t += dt
    displacement /= (2 * math.pi / omega) / dt
    return B * displacement

def wave(y):
    return SSA(y) + SSB(y)

def intensity(y):
    return wave(y) ** 2

Y = []
I = []

for i in range(-192, 192):
    Y.append(-i)
    I.append(intensity(i))

# Normalising I values

I_normalised = []

for value in I:
    I_normalised.append(value / max(I))

fig = plt.figure()

plot = fig.add_subplot(111)

plot.scatter(
    x=Y,
    y=I_normalised
)


plt.show()