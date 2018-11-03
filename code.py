import math

v = 340
D = 248
k = 244
l = 39
A = 39
B = 39
S = 9

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

omega = 2 * math.pi / l * v

period = 2 * math.pi / omega

def convert_decibel_to_intensity(dB):
    return 10 ** (-12) * 10 ** (dB / 10)

def convert_intensity_to_decibel(intensity):
    return 10*math.log10(intensity * 10**(12))


def d_a(x):
    return math.sqrt(D**2 + (x - (B + S) / 2)**2)

def d_b(x):
    return math.sqrt(D**2 + (x + (A + S) / 2)**2)


def phi(x):
    return abs(math.pi / l * (d_b(x) - d_a(x)))

def I(x):
    return (1/k**2) * (A**2 / (d_a(x))**4 + 2*A*B*math.cos(phi(x)) / ((d_a(x))**2 * (d_b(x))**2) + B**2 / (d_b(x))**4)

# Measured values from text file
X = []
Y = []

# Lists for predicted values
tx = []
ty = []


# Generate a theoretical prediction
# of the y value for each x value measured experimentally
i = 0
while (i < len(X)):
    tx.append(X[i])
    ty.append(I(X[i]))
    i += 1

# Normalise the measured y-values to fit in [0, 1]
y_max = max(Y)
i = 0
while i < len(Y):
    Y[i] = Y[i] / y_max
    i += 1

# Normalise the theoretically predicted y-values to fit in [0, 1]
i = 0
ty_max = max(ty)
while i < len(ty):
    ty[i] = ty[i] / ty_max
    i += 1