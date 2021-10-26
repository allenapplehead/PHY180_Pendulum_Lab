# Converts Tracker data into the correct format for fitter.py
# Also solves for Q by counting oscillations until initial amplitude decays
# to theta_i * e^(-pi/n)

# Author: Allen Tao
# PHY180 Pendulum Lab

import math

## Toggle this to generate data for the decaying amplitude graph
ampOnly = True

## Variables for calculating Q
theta_initial = 1e9 # will be updated later in the program
tgt_angle = 1e9 # = theta_initial * e^(-pi/decay), updated later in program
decay = 3.0 # e^-pi/decay
osc = 0 # variable to count number of half-periods (half-oscillations) ie: swinging from
        # one extreme to another

# Uncertainties
t_unc = 0.5 * 1.0 / 30.0 # Half frame rate estimate for time uncertainty
delta_x = 1.319 * 0.01
delta_y = 0.8215 * 0.01

# Take every n frames
skip = 2

# Only start taking data once the amplitude is the below value
theta_thres = 0.80
begin_logging = False

# Take how many samples? -1 means take as many samples as there are from tracker raw data
samples = -1

delta_thres = 0.05
blockout = 10 # Stop looking for amplitude for the next n frames after detecting one
shutoff = 0

# If data is not taken exactly at the beginning
t_offset = 0

# Open the raw data from tracker
fileName = "t0"
f = open(fileName + ".txt", "r")

new_data = [] # Format: time, angle, unc_time, unc_angle
counter = 0 # Number of lines parsed
prev_ang = 1e9 # Stores previous angle

killLoop = False

def detect_amplitude(cur_ang):
    if abs(cur_ang) - abs(prev_ang) <= delta_thres:
        return True
    return False

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
        cur_ang = math.atan(x / y)

        # Propagate the associated uncertainty
        delta_theta = abs(max(delta_x / abs(x), delta_y / abs(y)) * cur_ang)

        upd = [float(l[0]), cur_ang, t_unc, delta_theta]
        
        #print("DEBUG:", cur_ang)

        # Detect max angles
        if (counter == 2) or (shutoff == 0 and prev_ang != 1e9 and detect_amplitude(cur_ang)):
            osc += 1
            shutoff = blockout

            if not begin_logging and cur_ang >= 0 and cur_ang <= theta_thres:
                begin_logging = True
                # set the initial and target angle
                theta_initial = cur_ang
                tgt_angle = theta_initial * math.e ** (-math.pi / decay)
                print("Initial amplitude:", theta_initial)
                print("Target amplitude:", tgt_angle)

                # account for time offsets
                if upd[0] != 0:
                    t_offset = upd[0]

            if begin_logging and abs(cur_ang) <= abs(tgt_angle):
                killLoop = True # The program will stop running once it finishes this iteration of the loop

            if ampOnly:
                # If we want to graph amplitudes only, then we discard any non-amplitude values
                upd[1] = abs(upd[1])
                upd[0] -= t_offset
                new_data.append(upd)
        elif ampOnly:
            pass
        elif begin_logging:
            upd[0] -= t_offset
            new_data.append(upd)

        prev_ang = cur_ang

    counter += 1

print("Parsed", counter - 2, "lines.")
full_osc = osc // 2 + 1
if (osc % 2 == 0):
    full_osc -= 1
print("Full oscillations to get to e^(-pi/" + str(decay) + "):", full_osc)
# Full oscillation is defined as the bob travelling from one extreme to the other and back
f.close()

# Write the data in a properly formatted way to the output file
g = open(fileName + "out.txt", "w")

for line in new_data:
    for i in range(4):
        g.write(str(round(line[i], 4)))
        if i < 4 - 1:
            g.write(" ")
    g.write("\n")

g.close()