import math
import plotly.offline as py
import plotly.graph_objs as go

print("Application started")

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


print("Use default parametres? (say yes if grabbing parametres from a text file)")
res = input()
if (res.startswith('n')):
    print(f"Distance from slits to screen in cm (default: {D})")
    res = input()
    if is_number(res):
        D = float(res)

    print(f"Distance from source to slits in cm (default: {k})")
    res = input()
    if is_number(res):
        k = float(res)

    print(f"Wavelength in cm (default: {l})")
    res = input()
    if is_number(res):
        l = float(res)

    print(f"Width of slit A in cm (default: {A})")
    res = input()
    if is_number(res):
        A = float(res)

    print(f"Width of slit B in cm (default: {B})")
    res = input()
    if is_number(res):
        B = float(res)

    print(f"Width of separator in cm (default: {S})")
    res = input()
    if is_number(res):
        S = float(res)


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


print("Creating lists...")
# Lists for measured values
X = []
Y = []

# Lists for predicted values
tx = []
ty = []

values = []
points = []

print("Input your values - Type 'done' when finished, or reference a .txt file in data/experimental")
value = input()

if ('.txt' in value):
    print("Grab experimental parametres from text file? no if no")
    res = input()

    data_filename = value
    data_file = open(f"data/experimental/{data_filename}")
    data_lines = data_file.readlines()
    print(f"data_lines: {data_lines}")

    if (not res.startswith('n')):
        # Grab experimental parametres from text file
        parametres_line = data_lines[0]
        parametres_and_equals_signs = parametres_line.split(',')
        parametres = []
        for parametre in parametres_and_equals_signs:
            parametres.append(parametre.split('=')[1])
        D = float(parametres[0])
        k = float(parametres[1])
        l = float(parametres[2])
        A = float(parametres[3])
        B = float(parametres[4])
        S = float(parametres[5])
    i = 3
    while (i < len(data_lines)):
        print(f"Data line: {data_lines[i]}")
        values.append([float(data_lines[i].split(' ')[0]),
                       float(data_lines[i].split(' ')[6])])
        X.append(float(data_lines[i].split(' ')[0]))
        Y.append(convert_decibel_to_intensity(
            float(data_lines[i].split(' ')[6])))
        i += 1
else:
        # Convert values to floats and add to list --> values array
    while value != 'done':
        values.append([float(value.split(',')[0]), float(value.split(',')[1])])
        value = input()

    for point in values:
        points.append([point[0], convert_decibel_to_intensity(point[1])])

    for point in points:
        X.append(point[0])
        Y.append(point[1])

print("Type the filename to save the data to")
filename = input()

print("Defining layout...")
# Define layout for plot
layout = go.Layout(
    title=f"D={D}, k={k}, λ={l}, A={A}, B={B}, S={S}",
    xaxis=dict(
        title="Distance from center (cm)",
    ),
    yaxis=dict(
        title="Intensity"
    )
)

print("Generating theoretical prediction...")
# Generate a theoretical prediction
# of the y value for each x value measured experimentally
i = 0
while (i < len(X)):
    tx.append(X[i])
    ty.append(I(X[i]))
    if (int(round(i + 1 / len(X))) > int(round(i / len(X)))):
        print(f"{int(round((i + 1) / len(X) * 100))}%")
    i += 1

print("Saving data to text file...")

print("Name of file to save only experimental data to")
experiment_filename = input()

if (experiment_filename):
    experimental_file = open(f"data/experimental/{filename}.txt", "w")

    print(
        f"Saved experimental data to data/experimental/{experiment_filename}")

    # Write parametres
    experimental_file.write("%s\n" %
                            f"D={D}, k={k}, lambda={l}, A={A}, B={B}, S={S}"
                            )

    # Write header 'Experimental'
    experimental_file.write("\n%s\n" %
                            'Experimental'
                            )
    # Loop over measured values and save them to text file
    i = 0
    while i < len(X):
        experimental_file.write("%s\n" %
                                f'{X[i]}      {values[i][1]} dB'
                                )
        i += 1


# Save data to text file:
thefile = open(f'data/{filename}.txt', 'w')

# Write parametres
thefile.write("%s\n" %
              f"D={D}, k={k}, lambda={l}, A={A}, B={B}, S={S}"
              )

print("Saving experimental data")

# Write header 'Experimental'
thefile.write("\n%s\n" %
              'Experimental'
              )
# Loop over measured values and save them to text file
i = 0
while i < len(X):
    thefile.write("%s\n" %
                  f'{X[i]}      {values[i][1]} dB      {Y[i]}'
                  )
    i += 1

print("Saving theoretical data")

# Write header 'Theory'
thefile.write('\n%s\n' % 'Theory')

# Loop over predicted values and save them to text file
i = 0
while i < len(X):
    thefile.write("%s\n" %
                  f'{tx[i]}      {convert_intensity_to_decibel(ty[i])} dB      {ty[i]}')
    i += 1

print("Normalising experimental values...")
# Normalise the measured y-values to fit in [0, 1]
y_max = max(Y)
i = 0
while i < len(Y):
    Y[i] = Y[i] / y_max
    i += 1

print("Normalising theoretical values")
# Normalise the theoretically predicted y-values to fit in [0, 1]
i = 0
ty_max = max(ty)
while i < len(ty):
    ty[i] = ty[i] / ty_max
    i += 1

print("Saving normalised experimental data")

# Write header 'Normalised experimental'
thefile.write("\n%s\n" %
              'Normalised Experimental'
              )
# Loop over measured values and save them to text file
i = 0
while i < len(X):
    thefile.write("%s\n" %
                  f'{X[i]}      {values[i][1]} dB      {Y[i]}'
                  )
    i += 1

print("Saving normalised theoretical values")

# Write header 'Normalised theory'
thefile.write('\n%s\n' % 'Normalised Theory')

# Loop over predicted values and save them to text file
i = 0
while i < len(X):
    thefile.write("%s\n" %
                  f'{tx[i]}      {convert_intensity_to_decibel(ty[i])} dB      {ty[i]}')
    i += 1

print("Creating traces...")

# Create a trace 'Experimental' for the measured values
experimental = go.Scatter(
    x=X,
    y=Y,
    name="Experimental"
)
# Create a trace 'Theory' for the theoretically predicted values
theory = go.Scatter(
    x=tx,
    y=ty,
    name='Theory without diffraction'
)

print("Creating data from traces...")

# Create the data from the traces
data = [experimental, theory]

print("Creating figures using data and layout...")

# Create the figure using the data and layout
fig = go.Figure(data=data, layout=layout)

print("Plotting the figure and saving to html file")

# Plot the figure and save to html file
py.plot(fig, filename=f'plots/{filename}.html')

print(f"Plot saved to plots/{filename}.html ")
