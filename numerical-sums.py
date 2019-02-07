import math
import plotly.offline as py
import plotly.graph_objs as go

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

A = 26
B = 52
S = 9
D = 248
k = 244
wavelength = 548

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
    return math.sqrt(D ** 2 + (y + i * A / ( n - 1) - (B + S) / 2) ** 2)

# Distance from ith source in slit B to point with displacement y,
# as calculated in paper.
# 0th source is in the middle, -(n - 1) /2 at the top, ,and (n - 1) / 2 at the bottom.
def d_bi(i, y):
    return math.sqrt(D ** 2 + (y + i * B  / (n - 1) + (A + S) / 2) ** 2)

# Converting a path difference between two waves to a point to a phase shift
def phase_shift(path_difference):
    return 2 * math.pi / wavelength * path_difference

# Gives the wave contributed by the ith source from slit A at a certain point at a specific time.
# The amplitude should be A / (d_a^2) as calculated in the paper, but we multiply by A
# later in the code so we don't have to do it many times
def partial_A(i, y, t):
    return math.sin(omega * t + phase_shift(d_a(y) - d_ai(i, y))) / (d_ai(i, y) ** 2)

# Gives the wave contributed by the ith source from slit B at a certain point at a specific time.
# The amplitude should be B / (d_b^2) as calculated in the paper, but we multiply by B
# later in the code so we don't have to do it many times
def partial_B(i, y, t):
    return math.sin(omega * t + phase_shift(d_b(y) - d_bi(i, y))) / (d_bi(i, y) ** 2)

# Calculates the sum of the waves contributed by all the sources from slit A 
# at the point with displacement y at a certain time t
def sum_A(y, t):
    displacement = 0
    # Summing from i = -(n -1) / 2 to (n - 1) / 2. Converting to
    # int because the division yields a float
    for i in range(int(-(n - 1) / 2), int((n - 1) / 2)):
        displacement += partial_A(i, y, t)
    # Here we multiply by A, as 'promised' earlier
    displacement = displacement * A / n
    return displacement

# Calculates the sum of the waves contributed by all the sources from slit B
# at the point with displacement y at a certain time t
def sum_B(y, t):
    displacement = 0
    for i in range(int(-(n - 1) / 2), int((n - 1) / 2)):
        # For each source, add the displacement contributed to the total
        # displacement
        displacement += partial_B(i, y, t)
    # Here we multiply by B as 'promised' earlier
    displacement = displacement * B / n
    # Return the displacement of the resultant wave at the point with displacement y at
    # time t
    return displacement

# Creating lists for the plot
Y = []
I = []


# Returns the square of the displacement of the superposition of the resultant waves
# from both slits at the point with displacement t, at a given time t
def square_displacement(y, t):
    return (sum_A(y, t) + sum_B(y, t)) ** 2

# Numerical integration of square_displacement(y, t) from t = 0 to t = 2pi / omega.
# Then dividing by 2pi / omega gives the average
# This will be proportional to the intensity, and thus will 'be' the intensity
# since we are using relative units
def average_square_displacement(y):
    t = 0
    average_of_square_displacement = 0
    slices = 10
    upper_bound = 2 * math.pi / omega
    dt = upper_bound / slices
    while t <= upper_bound:
        result += average_of_square_displacement(y, t)
        t += dt
    average_of_square_displacement /= slices
    return result

# Since the experiment measured intensity values for displacement values ranging
# from -192 to 192, do the same here
for i in range(-192, 192):
    # Simply append the displacement to this list. So the list will be
    # Y = [-192, -191, ..., 3, 2, 1, 0, 1, 2, 3, ..., 191, 192]
    Y.append(i)
    # For each displacement value, use the intensity function defined earlier to predict
    # the intensity at that point, then add it to the list I
    I.append(average_square_displacement(i))

I_normalised = []

for value in I:
    # I_normamlised will keep the shape/characteristics of I when plotted,
    # but the maximum will be 1
    I_normalised.append(value / max(I))

# Define layout for plot
layout = go.Layout(
    title=f"D={D}, k={k}, λ={wavelength}, A={A}, B={B}, S={S}",
    xaxis=dict(
        title="Distance from center (cm)",
    ),
    yaxis=dict(
        title="Intensity"
    )
)

# Plot the model
diffraction = go.Scatter(
    x=Y,
    y=I_normalised,
    name="Theory with diffraction"
)

data = [diffraction]

fig = go.Figure(data=data, layout=layout)

# Save the diagram
print("Name of file to save diagram to:")
filename = input()

if '.html' not in filename:
    filename = f'{filename}.html'

py.plot(fig, filename=f'diagrams/diffraction/{filename}')

print(f'Plot saved to diagrams/diffraction/{filename}')