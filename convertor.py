# Converts Tracker data into the correct format for fitter.py
# Also solves for Q by counting oscillations until initial amplitude decays
# to theta_i * e^(-pi/n)

# Author: Allen Tao
# PHY180 Pendulum Lab

import math

## Variables for calculating Q
theta_initial = 1e9 # will be updated later in the program
tgt_angle = 1e9 # = theta_initial * e^(-pi/decay), updated later in program
decay = 4.0 # e^-pi/4
osc = 0 # variable to count number of half-periods (half-oscillations) ie: swinging from
        # one extreme to another

# Uncertainties
t_unc = 0.033
ang_unc = 0.001

# Take every n frames
skip = 1

# Take how many samples? -1 means take as many samples as there are from tracker raw data
samples = -1

# List and variables to help recognize when the bob has swung to one extreme or another
# Noise is taken into account and mitigated through recording the last 5 values,
# and verifying that the value 3 values ago is larger than the last value and
# the value 5 values ago. This irons out minor fluctuations in the angle from 
# raw tracker data
pastAngles = [] # Keeps the 5 most recent angles
blockout = 5 # Stop looking for amplitude for the next n frames after detecting one
shutoff = 0

# Open the raw data from tracker
f = open("data.txt", "r")

new_data = [] # Format: time, angle, unc_time, unc_angle
counter = 0 # Number of lines parsed
prev_ang = 1e9 # Stores previous angle

for line in f:
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
        sgn = 1
        tmp = -1 * float(l[2]) / (1 * math.sqrt(float(l[1]) ** 2 + float(l[2]) ** 2))
        if float(l[1]) < 0:
            sgn *= -1
        cur_ang = sgn * float(math.acos(tmp))
        upd = [float(l[0]), cur_ang, t_unc, ang_unc]
        
        if theta_initial == 1e9:
            # set the initial angle
            theta_initial = cur_ang
            tgt_angle = theta_initial * math.e ** (-math.pi / decay)
        
        # Detect max angles
        if (counter == 2) or shutoff == 0 and len(pastAngles) >= 5 and abs(pastAngles[-3]) > abs(pastAngles[-1]) and abs(pastAngles[-3]) > abs(pastAngles[-5]):
            """
            if len(pastAngles) >= 5:
                print("Last 5 values:")
                for i in range(1, 6):
                    print(pastAngles[-i], "Counter:", counter - i)
            """
            osc += 1
            shutoff = blockout
            if len(pastAngles) >= 5 and pastAngles[-3] <= tgt_angle:
                samples = 1e9 # The program will stop running once it finishes this iteration of the loop

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