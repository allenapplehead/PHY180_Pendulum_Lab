# Converts Tracker data into the correct format for fitter.py
# Also solves for Q by counting oscillations until initial amplitude decays
# to theta_i * e^(-pi/n)

# Author: Allen Tao
# PHY180 Pendulum Lab

import math

## Variables for calculating Q
theta_initial = 1e9 # will be updated later in the program
tgt_angle = 1e9 # = theta_initial * e^(-pi/decay), updated later in program
decay = 3.0 # e^-pi/decay
osc = 0 # variable to count number of half-periods (half-oscillations) ie: swinging from
        # one extreme to another

# Uncertainties
t_unc = 0.033 / 2.0 # Half frame rate estimate for time uncertainty
delta_x = 1.319
delta_y = 0.8215

# Take every n frames
skip = 2

# Take how many samples? -1 means take as many samples as there are from tracker raw data
samples = -1

# List and variables to help recognize when the bob has swung to one extreme or another
# Noise is taken into account and mitigated through recording the last r values,
# and verifying that the value r // 2 + 1 values ago is larger than the last value and
# the value r values ago. This irons out minor fluctuations in the angle from 
# raw tracker data
r = 5 # Make sure r is an odd number
pastAngles = [] # Keeps the 5 most recent angles
blockout = 10 # Stop looking for amplitude for the next n frames after detecting one
shutoff = 0

# Open the raw data from tracker
f = open("data.txt", "r")

new_data = [] # Format: time, angle, unc_time, unc_angle
counter = 0 # Number of lines parsed
prev_ang = 1e9 # Stores previous angle

killLoop = False

for line in f:
    if killLoop:
        break

    # Only take samples samples
    if samples > 0 and (counter - 2) > samples:
        break

    # We skip the first two lines, no numerical data there
    if counter < 2:
        counter += 1
        continue
    
    # We take data for every skip frames
    if (counter - 2) % skip == 0:
        if shutoff > 0:
            shutoff -= 1
        # Parse the line
        l = line.split()

        ## Idea: use angle between 2 vectors formula to find the angle between the string
        # and the vertical
        # v = [0, -1]
        # w = [l[1],l[2]]
        x = float(l[1])
        y = float(l[2])
        sgn = 1
        tmp = -1 * y / (math.sqrt(x ** 2 + y ** 2))

        # Propagate the associated uncertainty
        delta_theta = abs(max(delta_y / y, max(delta_x / x * x ** 2, delta_y / y * y ** 2) / (x ** 2 + y ** 2)) * tmp)

        if x < 0:
            sgn *= -1
        cur_ang = sgn * float(math.acos(tmp))
        upd = [float(l[0]), cur_ang, t_unc, delta_theta]
        
        if theta_initial == 1e9:
            # set the initial angle
            theta_initial = cur_ang
            tgt_angle = theta_initial * math.e ** (-math.pi / decay)
            print("Initial amplitude:", theta_initial)
            print("Target amplitude:", tgt_angle)
        
        # Detect max angles
        if (counter == 2) or shutoff == 0 and len(pastAngles) >= r and abs(pastAngles[-(r // 2 + 1)]) >= abs(pastAngles[-1]) and abs(pastAngles[-(r // 2 + 1)]) >= abs(pastAngles[-r]):
            osc += 1
            shutoff = blockout
            if len(pastAngles) >= r and abs(pastAngles[-(r // 2 + 1)]) <= abs(tgt_angle):
                killLoop = True # The program will stop running once it finishes this iteration of the loop

        pastAngles.append(cur_ang)
        new_data.append(upd)
    counter += 1

print("Parsed", counter - 2, "lines.")
full_osc = osc // 2 + 1
if (osc % 2 == 0):
    full_osc -= 1
print("Full oscillations to get to e^(-pi/" + str(decay) + "):", full_osc)
# Full oscillation is defined as the bob travelling from one extreme to the other and back
f.close()

# Write the data in a properly formatted way to the output file
g = open("out.txt", "w")

for line in new_data:
    for i in range(4):
        g.write(str(round(line[i], 4)))
        if i < 4 - 1:
            g.write(" ")
    g.write("\n")

g.close()