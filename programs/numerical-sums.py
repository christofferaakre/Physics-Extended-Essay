import math
import matplotlib.pyplot as plt

# Experimental parametres
    # Parametres matching experimental trials:        
        # Trial 1 - Single slit with small lambda: 
            # A = 87,5, B = 0, S = 0, D = 248, wavelength = 87,5
        # Trial 2 - Single slit with large lambda: 
            # A = 87.5, B = 0, S = 0, D = 248, wavelength = 227
        # Trial 3 - Double slit, equal width with small lambda:
            # A = 39, B = 39, S = 9, D = 248, wavelength = 39
        # Trial 4 - Double slit, equal width, with large lambda:
            # A = 39, B = 39, S = 9, D = 248, wavelength = 548
        # Trial 5 - Double slit, one slit twice the width of the other, with large lambda:
            # A = 26, B = 52, S = 9, D = 248, wavelength = 548

# Note: All distances measured in cm. Speeds in cm/s

A = 87.5
B = 0
S = 0
D = 248
wavelength = 227

# Speed of sound is approx. 340 m/s --> 340 * 100 cm/s
v = 340 * 100

omega = 2 * math.pi * v / wavelength

# Number of sources to use for each slit with Huygen's Principle
n = 25

# Distance from centre of slit A to point with displacement y, as calculated
# in paper
def d_a(y):
    return math.sqrt(D ** 2 + (y - (B + S) / 2) ** 2)

# Distance from centre of slit B to point with displacement y,
# as calculated in paper
def d_b(y):
    return math.sqrt(D **  2 + (y + (A + S) / 2) ** 2)


# Distance from ith source in slit A to point with displacement y,
# as calculated in paper. 
# 0th source is in the middle, -(n - 1) /2 at the top, ,and (n - 1) / 2 at the bottom.
def d_ai(i, y):
    return math.sqrt(D ** 2 + (y + i * A / ( n - 1) - (B + S) / 2) * 2)

# Distance from ith source in slit B to point with displacement y,
# as calculated in paper.
# 0th source is in the middle, -(n - 1) /2 at the top, ,and (n - 1) / 2 at the bottom.
def d_bi(i, y):
    return math.sqrt(D ** 2 + (y + i * B  / (n - 1) + (A + S) / 2) ** 2)

# Converting a path difference between two waves to a point to a phase shift
def phase_shift(path_difference):
    return 2 * math.pi / wavelength * path_difference

# Gives the wave contributed by the ith source from slit A at a certain point at a specific time.
# The amplitude should be A / (d_a^2) as calculated in the paper, but we multiply by this term
# later in the code so we don't have to do it many times
def partial_A(i, y, t):
    return math.sin(omega * t + phase_shift(d_a(y) - d_ai(i, y)))

# Gives the wave contributed by the ith source from slit B at a certain point at a specific time.
# The amplitude should be B / (d_b^2) as calculated in the paper, but we multiply by this term
# later in the code so we don't have to do it many times
def partial_B(i, y, t):
    return math.sin(omega * t + phase_shift(d_b(y) - d_bi(i, y)))

# Calculates the sum of the waves contributed by all the sources from slit A 
# at the point with displacement y at a certain time t
def sum_A(y, t):
    displacement = 0
    for i in range(int(-(n - 1) / 2), int((n - 1) / 2)):
        displacement += partial_A(i, y, t)
    displacement /= (n * (d_a(y) ** 2))
    return displacement

# Calculates the sum of the waves contributed by all the sources from slit B
# at the point with displacement y at a certain time t
def sum_B(y, t):
    displacement = 0
    # Summing from i = -(n -1) / 2 to (n - 1) / 2. Converting to
    # int because the division yields a float
    for i in range(int(-(n - 1) / 2), int((n - 1) / 2)):
        # For each source, add the displacement contributed to the total
        # displacement
        displacement += partial_B(i, y, t)
    displacement /= (n * (d_b(y) ** 2))
    # Return the displacement of the resultant wave at the point with displacement y at
    # time t
    return displacement

Y = []
I = []

# Numerical integration of sum_A, which is the displacement of the resultant wave coming from slit A at the point
# with displacement y at a time t, from 0 to 2pi / omega to get the actual displacement
# contributed by slit A at the point with displacement y
def displacement_A(y):
    t = 0
    displacement = 0
    slices = 10
    upper_bound = 2 * math.pi / omega
    dt = upper_bound / slices
    while t <= upper_bound:
        displacement += sum_A(y, t)
        t += dt
    displacement /= slices
    return  A * displacement

# Numerical integration of sum_B, which is the displacement of the resultant wave coming from slit B at the point
# with displacement y at a time t, from 0 to 2pi / omega to get the actual displacement
# contributed by slit B at the point with displacement y
def displacement_B(y):
    t = 0
    displacement = 0
    slices = 10
    upper_bound = 2 * math.pi / omega
    dt = upper_bound / slices
    while t <= upper_bound:
        displacement += sum_B(y, t)
        t += dt
    displacement /= slices
    return B * displacement

# Return the displacement of the superposition of the resultant waves coming from slits
# A and B
def wave(y):
    return displacement_A(y) + displacement_B(y)

# To get the intensity, square the displacement of the superposition
def intensity(y):
    return wave(y) ** 2

# Since the experiment measured intensity values for displacement values ranging
# from -192 to 192, do the same here
for i in range(-192, 192):
    # Simply append the displacement to this list. So the list will be
    # Y = [-192, -191, ..., 3, 2, 1, 0, 1, 2, 3, ..., 191, 192]
    Y.append(i)
    # For each displacement value, use the intensity function defined earlier to predict
    # the intensity at that point, then add it to the list I
    I.append(intensity(i))

I_normalised = []

for value in I:
    # I_normamlised will keep the shape/characteristics of I when plotted,
    # but the maximum will be 1
    I_normalised.append(value / max(I))

# Plot the graph
plot = plt.scatter(
    x=Y,
    y=I_normalised
)

# Show the graph
plt.show()