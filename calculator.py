# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ___________________________________________________                         #
#< Mannan Sethia 2020 - Generic Trajectory calculator >                       #
# ---------------------------------------------------                         #
#      \                    / \  //\                                          #
#       \    |\___/|      /   \//  \\                                         #
#            /0  0  \__  /    //  | \ \                                       #
#           /     /  \/_/    //   |  \  \                                     #
#           @_^_@'/   \/_   //    |   \   \                                   #
#           //_^_/     \/_ //     |    \    \                                 #
#        ( //) |        \///      |     \     \                               #
#      ( / /) _|_ /   )  //       |      \     _\                             #
#    ( // /) '/,_ _ _/  ( ; -.    |    _ _\.-~        .-~~~^-.                #
# (( / / )) ,-{        _      `-.|.-~-.           .~         `.               #
#(( // / ))  '/\      /                 ~-. _ .-~      .-~^-.  \              #
#(( /// ))      `.   {            }                   /      \  \             #
# (( / ))     .----~-.\        \-'                 .~         \  `. \^-.      #
#             ///.----..>        \             _ -~             `.  ^-`  ^-_  #
#               ///-._ _ _ _ _ _ _}^ - - - - ~                     ~-- ,.-~   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# -------------------------- INPUT (ARGUMENTS) ----------------------------- #

import argparse
import sys
import math
import matplotlib.pyplot as plt
import numpy
import tkinter as tk

desc1 = 'A generic calculator of projectile trajectories. '
desc2 = 'See wiki at www.---.com for more information and explanations for parameters and usage. '
desc3 = 'Does not account for drag!'
parser = argparse.ArgumentParser(description=desc1+desc3)


# Required parameters
parser.add_argument('-p', type=str,
    help='Some preset projectiles from different weapons. Setting mass or speed will override the preset mass / speed.',
    choices=['ak47', 'glock17', 'coltpeacemaker', 'uzi', 'railgun', '18thcenturycannon', 'barettm82'], required=False)
parser.add_argument('-a', type=float,
    help='Angle of projectile movement in degrees (°) where 0° = directly forwards, and 90° = directly upwards', required=False)
parser.add_argument('-s', type=float,
    help='Speed of projectile in metres / second (m/s)', required=False)

# Optional parameters
parser.add_argument('-m', type=float,
    help='(Optional) Mass of projectile in grams (g)', required=False)
parser.add_argument('-e', type=float,
    help='(Optional, defaults to zero) Intial projectile elevation in metres (m)', required=False, default=0)
parser.add_argument('-x', type=float,
    help='(Optional) Elevation of projectile at specified distance', required=False)
parser.add_argument('-g', type=float,
    help='(Optional, defaults to Earth) Gravitational field strength (g)', required=False, default=9.81)
parser.add_argument('-i', type=str,
    help='(Optional) Approximate impact surface area of projectile: Small = bullet, medium = football, large = small asteroid',
    choices=['small', 'medium', 'large'], required=False)
parser.add_argument('-d', type=str,
    help='(Optional) Accuracy of estimation of distance travelled (low = intervals of 10%% of total displacement, medium = 1%%, high = 0.1%%)',
    choices=['low', 'medium', 'high'], required=False)

parser.add_argument('--im', action='store_true',
    help='Pass this argument to use pounds (lb) instead of grams (g) to measure mass', required=False)
parser.add_argument('--iv', action='store_true',
    help='Pass this argument to use miles per hour (mph) instead of metres per second (m/s) to measure speed', required=False)
parser.add_argument('--id', action='store_true',
    help='Pass this argument to use feet (ft) instead of metres (m) to measure distance', required=False)
parser.add_argument('--gr', action='store_true',
    help='Pass this argument to show graph output', required=False)
parser.add_argument('--gui', action='store_true',
    help='Pass this argument launch the GUI version of the program. The GUI version is lighter (has fewer features)', required=False)

# Parsing and collecting arguments
args = parser.parse_args()
preset = args.p
mass = args.m
speed = args.s
angle = args.a
elevation = args.e
impact = args.i
distgap = args.d
gravity = args.g
altmass = args.im
altspeed = args.iv
altdist = args.id
graphyn = args.gr
guiyn = args.gui


# ----------------------- GUI version of application ----------------------- #

if guiyn == True:
    # Init
    gui = tk.Tk()
    gui.title('Generic trajectory calculator')

    # Function code
    def exe():
        # Refreshing text box
        text.delete('1.0', tk.END)

        # Storing input
        guimass = int(float(entry1.get()))
        guispeed = int(float(entry2.get()))
        guiangle = int(float(entry3.get()))
        guielev = int(float(entry4.get()))
        guigrav = int(float(entry5.get()))
        guiacc = str(var1.get())
        guigraph = bool(var2.get())

        # Validating input
        if guiangle < 0 or guiangle > 90:
            text.insert('1.0', 'Error: angle out of range')

        # Horizontal component of projectile
        if guiangle == 90:
            guihorizontal = 0
        elif guiangle == 0:
            guihorizontal = guispeed
        else:
            guihorizontal = math.cos(math.radians(guiangle)) * guispeed

        # Vertical component of projectile
        if guiangle == 90:
            guivertical = guispeed
        elif guiangle == 0:
            guivertical = 0
        else:
            guivertical = math.sin(math.radians(guiangle)) * guispeed

        # Intial and final vertical velocities
        guivinitvelocity = guivertical
        if guielev != 0:
            guivfinalvelocity = math.sqrt((guivinitvelocity ** 2) + (2 * guigrav * guielev))
        else:
            guivfinalvelocity = guivinitvelocity

        # Projectile air time
        guivdeltavelocity = guivfinalvelocity + guivinitvelocity
        guiairtime = guivdeltavelocity / guigrav

        # Horizontal displacement
        guidisplacement = guihorizontal * guiairtime

        # Maximum height reached
        guimaxheight = (guivinitvelocity ** 2) / (2 * guigrav)
        guimaxheight = guimaxheight + guielev
        if guivinitvelocity < 0:
            guimaxheight = guielev

        # Energy on impact
        guienergy = 0.5 * guimass * (guispeed ** 2)

        # Approximating distance
        if guiacc == 'Low':
            distreps = 10
            distdecimal = 0.1
        if guiacc == 'Medium':
            distreps = 100
            distdecimal = 0.01
        if guiacc == 'High':
            distreps = 1000
            distdecimal = 0.001
        inita = guielev
        initd = 0

        for x in range(1, distreps+1):
            xinpos = distdecimal * guidisplacement * x
            axsquarednumerator = -0.5 * guigrav * (xinpos ** 2)
            axsquareddenominator = (math.cos(math.radians(guiangle)) ** 2) * (guispeed ** 2)
            bx = xinpos * math.tan(math.radians(guiangle))
            c = guielev
            fx = (axsquarednumerator / axsquareddenominator) + bx + c
            leny = fx - inita
            lenx = distdecimal * guidisplacement
            incidentlen = math.sqrt((leny ** 2) + (lenx ** 2))
            initd = initd + incidentlen

        # Printing Output
        text.insert('1.0', 'Horizontal displacement: ' + str(guidisplacement) + ' m' + '\n')
        text.insert('2.0', 'Air time: ' + str(guiairtime) +  's' + '\n')
        text.insert('3.0', 'Energy on impact: ' + str(guienergy) + ' J' + '\n')
        text.insert('4.0', 'Approximate distance travelled: ' + str(initd) + ' m' + '\n')


        # Plotting trajectory
        x = numpy.linspace(0, guidisplacement, 200)

        axsquarednumerator = -0.5 * guigrav * (x ** 2)
        axsquareddenominator = (math.cos(math.radians(guiangle)) ** 2) * (guispeed ** 2)
        bx = x * math.tan(math.radians(guiangle))
        c = guielev
        y = (axsquarednumerator / axsquareddenominator) + bx + c

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.set_aspect('equal', adjustable='box')
        fig.suptitle('Trajectory of projectile')
        plt.plot(x, y)
        plt.xlabel('Horizontal displacement (m)')
        plt.ylabel('Vertical displacement (m)')
        if guigraph == True:
            plt.show()


    # exit button Function
    def exitfunc():
        sys.exit()

    # Adding all options
    exitbutton = tk.Button(text='Exit', command=exit)
    label0 = tk.Label(text='All fields must be filled.')
    labelspace = tk.Label(text='')
    label1 = tk.Label(text='Mass (g)')
    entry1 = tk.Entry()
    label2 = tk.Label(text='Speed (m/s)')
    entry2 = tk.Entry()
    label3 = tk.Label(text='Angle (degrees)')
    entry3 = tk.Entry()
    label4 = tk.Label(text='Elevation (m)')
    entry4 = tk.Entry()
    label5 = tk.Label(text='Gravity (g)')
    entry5 = tk.Entry()

    var1 = tk.StringVar()
    label6 = tk.Label(text='Accuracy of estimation of distance (SELECT)')
    entry6 = tk.OptionMenu(gui, var1, 'Low', 'Medium', 'High')

    var2 = tk.IntVar()
    entry7 = tk.Checkbutton(text='Display graph of trajectory', variable=var2, onvalue=1, offvalue=0)

    button = tk.Button(text='Submit', command=exe)
    text = tk.Text()

    # Packing elements
    exitbutton.pack()
    labelspace.pack()
    label0.pack()
    label1.pack()
    entry1.pack()
    label2.pack()
    entry2.pack()
    label3.pack()
    entry3.pack()
    label4.pack()
    entry4.pack()
    label5.pack()
    entry5.pack()
    label6.pack()
    entry6.pack()
    entry7.pack()
    button.pack()
    text.pack()

    # Initialising event listener, end of code exec for GUI program --
    gui.mainloop()


# -------------------- End of GUI: Preparing parameters -------------------- #

# Converting all measures into metric
sm = ' m/s'
dm = ' m'
if altmass == True:
    if mass != None:
        mass = mass * 453.59
if altspeed == True:
    speed = speed / 2.2369
    sm = ' mph'
if altdist == True:
    elevation = elevation / 3.281
    dm = ' ft'

# Applying preset values to speed and mass
if preset == 'ak47':
    speed = 880
    mass = 3.43
    pressurearea = 0.000001
if preset == 'glock17':
    speed = 360
    mass = 7.45
    pressurearea = 0.000001
if preset == 'coltpeacemaker':
    speed = 343
    mass = 10
    pressurearea = 0.000001
if preset == 'uzi':
    speed = 360
    mass = 7.45
    pressurearea = 0.000001
if preset == 'railgun':
    speed = 3390
    mass = 10000
    pressurearea = 0.000001
if preset == '18thcenturycannon':
    speed = 175
    mass = 5443
    pressurearea = 0.000001
if preset == 'barettm82':
    speed = 928
    mass = 42
    pressurearea = 0.000001


# Applying preset values of impact area
pressurearea = None
if impact == 'small':
    pressurearea = 0.000001
if impact == 'medium':
    pressurearea = 0.1
if impact == 'large':
    pressurearea = 1000



# Errors, warnings, and information to do with parameter selection
if (preset == None) and (speed == None):
    print('Error: You must provide a speed, or select from the presets. Pass the --help argument to see all available parameters.')
    sys.exit()
    sys.exit()
if angle == None:
    print('Error: You must provide an angle of projectile movement')
    sys.exit()

if (angle < 0) or (angle > 90):
    print('Error: Angle must be between 0° and 90°')
    sys.exit()
if mass != None and mass < 0:
    print('Error: Mass must be a positive number')
    sys.exit()
if elevation != None and elevation < 0:
    print('Error: Elevation must be a positive number')
    sys.exit()
if gravity != None and gravity < 0:
    print('Error: Gravity must be a positive number')
    sys.exit()

if (preset != None) and (mass or speed != None):
    print('Warning: Setting a mass or speed while also selecting a preset will override the mass / speed from the preset.')
if altmass == True:
    print('Info: Measure of mass changed to pounds (lb)')
if altspeed == True:
    print('Info: Measure of speed changed to miles per hour (mph)')
if altdist == True:
    print('Info: Measure of distance / elevation changed to feet (ft)')


# ---------------- Executing calculations for input given ------------------ #

# Horizontal component of projectile
if angle == 90:
    horizontal = 0
elif angle == 0:
    horizontal = speed
else:
    horizontal = math.cos(math.radians(angle)) * speed

# Vertical component of projectile
if angle == 90:
    vertical = speed
elif angle == 0:
    vertical = 0
else:
    vertical = math.sin(math.radians(angle)) * speed

# Intial and final vertical velocities
vinitvelocity = vertical
if elevation != 0:
    vfinalvelocity = math.sqrt((vinitvelocity ** 2) + (2 * gravity * elevation))
else:
    vfinalvelocity = vinitvelocity

# Projectile air time
vdeltavelocity = vfinalvelocity + vinitvelocity
airtime = vdeltavelocity / gravity

# Horizontal displacement
displacement = horizontal * airtime

# Impact speed
impactspeed = math.sqrt((horizontal ** 2) + (vfinalvelocity ** 2))

# Angle of impact
if angle == 0:
    impactangle = 0
if angle == 90:
    impactangle = 0
else:
    impactangle = math.degrees(math.asin(horizontal / impactspeed))

# Maximum height reached
maxheight = (vinitvelocity ** 2) / (2 * gravity)
maxheight = maxheight + elevation
if vinitvelocity < 0:
    maxheight = elevation

# Time to reach maximum height
maxheighttime = vinitvelocity / gravity
if vinitvelocity < 0:
    maxheighttime = 0

# Horizontal displacement at max height
maxheightdist = maxheighttime * horizontal

# Energy on impact
if mass != None:
    energy = 0.5 * mass * (speed ** 2)

# Impact pressure
if mass != None:
    force = mass * gravity
if mass != None:
    if pressurearea != None:
        pressure = force / pressurearea


# Approximation of distance
if distgap == 'low':
    distreps = 10
    distdecimal = 0.1
if distgap == 'medium':
    distreps = 100
    distdecimal = 0.01
if distgap == 'high':
    distreps = 1000
    distdecimal = 0.001
inita = elevation
initd = 0

if distgap != None:
    for x in range(1, distreps+1):
        xinpos = distdecimal * displacement * x
        axsquarednumerator = -0.5 * gravity * (xinpos ** 2)
        axsquareddenominator = (math.cos(math.radians(angle)) ** 2) * (speed ** 2)
        bx = xinpos * math.tan(math.radians(angle))
        c = elevation
        fx = (axsquarednumerator / axsquareddenominator) + bx + c
        leny = fx - inita
        lenx = distdecimal * displacement
        incidentlen = math.sqrt((leny ** 2) + (lenx ** 2))
        initd = initd + incidentlen


# ---------------- Output of statistics for projectile --------------------- #

# Converting metric units to units of choice
if altspeed == True:
    horizontal = horizontal * 2.2369
    vertical = vertical * 2.2369
    impactspeed = impactspeed * 2.2369
if altdist == True:
    maxheight = maxheight * 3.281
    maxheightdist = maxheightdist * 3.281
    displacement = displacement * 3.281
    initd = initd * 3.281

# Printing results
print('# ---- Generic trajectory calculator ---- #')
print('\n')

print('Horizontal component of projectile: .   ' + str(horizontal) + sm)
print('Vertical component of projectile: ...   ' + str(vertical) + sm)
print('\n')

print('Horizontal displacement: ............    ' + str(displacement) + dm)
if altdist == True:
    displacement = displacement / 3.281

if displacement < 0.00001:
    print('... or approximately smaller than width of a white blood cell')
elif displacement < 0.0001:
    print('... or approximately the width of a human hair')
elif displacement < 0.001:
    print('... or approximately the width of an ant')
elif displacement < 0.01:
    print('... or approximately the diameter of a penny')
elif displacement < 0.1:
    print('... or approximately the diameter of a tennis ball')
elif displacement < 1:
    print('... or approximately the height of a human')
elif displacement < 10:
    print('... or approximately the length of a blue whale')
elif displacement < 100:
    print('... or approximately the length of an aeroplane')
elif displacement < 1000:
    print('... or approximately the length of the Vatican city')
elif displacement < 10000:
    print('... or approximately the height of Mount Everest')
elif displacement < 100000:
    print('... or approximately the length of the state of Texas')
elif displacement > 100000:
    print('... or approximately greater than the diameter of Pluto ')

print('Air time: ...........................    ' + str(airtime) + ' s')
print('\n')

print('Angle of impact: ....................    ' + str(impactangle) + '°')
print('Speed on impact: ....................    ' + str(impactspeed) + sm)
if altspeed == True:
    speed = speed / 2.2369
if speed < 0.001:
    print('... or approximately slower than speed of groundwater')
elif speed < 0.01:
    print('... or approximately the speed of a snail')
elif speed < 0.1:
    print('... or approximately the speed of a land turtle')
elif speed < 1:
    print('... or approximately the pace of walking')
elif speed < 10:
    print('... or approximately the speed of a sprinter')
elif speed < 100:
    print('... or approximately the speed of an arrow')
elif speed < 1000:
    print('... or approximately the speed of a bullet')
elif speed > 1000:
    print('... or approximately faster than the speed of a rocket')
print('\n')

print('Maximum height acheived: ............    ' + str(maxheight) + dm)
if displacement < 0.00001:
    print('... or approximately smaller than width of a white blood cell')
elif displacement < 0.0001:
    print('... or approximately the width of a human hair')
elif displacement < 0.001:
    print('... or approximately the width of an ant')
elif displacement < 0.01:
    print('... or approximately the diameter of a penny')
elif displacement < 0.1:
    print('... or approximately the diameter of a tennis ball')
elif displacement < 1:
    print('... or approximately the height of a human')
elif displacement < 10:
    print('... or approximately the length of a blue whale')
elif displacement < 100:
    print('... or approximately the length of an aeroplane')
elif displacement < 1000:
    print('... or approximately the length of the Vatican city')
elif displacement < 10000:
    print('... or approximately the height of Mount Everest')
elif displacement < 100000:
    print('... or approximately the length of the state of Texas')
elif displacement > 100000:
    print('... or approximately greater than the diameter of Pluto ')
print('Max height achieved after elapsed: ..    ' + str(maxheighttime) + ' s')
print('Max height achieved @ displacement: .    ' + str(maxheightdist) + dm)
print('\n')

if mass != None:
    print('Energy on impact: ...................    ' + str(energy) + ' J')
    if impact != None:
        print('Pressure on impact: .................    ' + str(pressure) + ' Pa')

if distgap != None:
    print('Approximate distance travelled: .....    ' + str(initd) + dm)
if graphyn == True:
    print('\n')
    print('Close the graph to terminate the program process.')


# Plotting trajectory
x = numpy.linspace(0, displacement, 200)

axsquarednumerator = -0.5 * gravity * (x ** 2)
axsquareddenominator = (math.cos(math.radians(angle)) ** 2) * (speed ** 2)
bx = x * math.tan(math.radians(angle))
c = elevation
y = (axsquarednumerator / axsquareddenominator) + bx + c

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_aspect('equal', adjustable='box')
fig.suptitle('Trajectory of projectile')
plt.plot(x, y)
plt.xlabel('Horizontal displacement (m)')
plt.ylabel('Vertical displacement (m)')
if graphyn == True:
    plt.show()
