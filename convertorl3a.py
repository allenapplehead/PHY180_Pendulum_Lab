# Converts Tracker data into the correct format for fitter.py
# Finds the period by counting a certain number oscillations
# from a certain release angle

# Author: Allen Tao
# PHY180 Pendulum Lab

import math

osc = 0 # variable to count number of half-periods (half-oscillations) ie: swinging from
        # one extreme to another

# Uncertainties
osc_to_count = 2
t_unc = (0.5 * 1.0 / 30.0) / osc_to_count # Half frame rate estimate for time uncertainty
delta_x = 1.319 * 0.01
delta_y = 0.8215 * 0.01

# Take every n frames
skip = 2

# Only start taking data once the amplitude is the below value
theta_thres = 0.150
begin_logging = False
t_start = 0
t_end = 0
cur_osc = 0
num_osc = 1 * 2

# Take how many samples? -1 means take as many samples as there are from tracker raw data
samples = -1

# Open the raw data from tracker
fileName = "LAB3/90"
f = open(fileName + ".txt", "r")

prev_x_delta = -1 # decreasing
pastX = []

cnt = 0
true_count = 0

for line in f:
    if cnt < 2:
        cnt += 1
        continue

    # Parse the line
    l = line.split()

    x = float(l[1])
    y = float(l[2])
    cur_ang = math.atan(x / y)

    # Propagate the associated uncertainty
    delta_theta = abs(max(delta_x / abs(x), delta_y / abs(y)) * cur_ang)

    upd = [float(l[0]), cur_ang, t_unc, delta_theta]

    # Determine if this angle is an amplitude
    if true_count == 0:
        print(cur_ang)

        if abs(cur_ang) < theta_thres:
            begin_logging = True
            t_start = upd[0]

        pastX.append(x)
        true_count += 1
        continue

    cur_delta = cur_ang - pastX[-1];
    sgn_cur_delta = 1
    if x - pastX[-1] < 0:
        sgn_cur_delta = -1
    pastX.append(x)

    if sgn_cur_delta != prev_x_delta:
        print(cur_ang)

        if abs(cur_ang) < theta_thres and not begin_logging:
            begin_logging = True
            t_start = upd[0]
        elif begin_logging:
            cur_osc += 1
            if cur_osc == num_osc:
                print("PERIOD:", upd[0] - t_start)
                break
        
        prev_x_delta = sgn_cur_delta
        osc += 1

    true_count += 1
    
print(osc)