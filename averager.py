# Takes the data from multiple trials, and averages them properly along with their uncs

# Allen Tao
# 10/24/2021

TRIALS = 3 # Use 0 indexed
out = []
fileName = "MASTER_DATA.txt"

for i in range(TRIALS):
    out.append([])

    # Open the right file
    f = open("t" + str(i) + "out.txt", "r")
    for line in f:
        out[i].append([float(item) for item in line.split()])
    f.close()

# Write the data
g = open(fileName, "w")
for i in range(min(len(out[0]), min(len(out[1]), len(out[2])))):
    res = [0, 0, 0, 0]
    avg = 0.0
    max_unc = 0.0
    # Extract time data
    for k in range(3):
        avg += out[k][i][0]
        max_unc = max(max_unc, out[k][i][2])
    avg /= 3.0
    res[0], res[2] = avg, max_unc

    # Extract angle data
    avg = 0.0
    max_unc = 0.0
    for k in range(3):
        avg += out[k][i][1]
        max_unc = max(max_unc, out[k][i][3])
    avg /= 3.0
    res[1], res[3] = avg, max_unc

    for i in range(4):
        g.write(str(round(res[i], 4)))
        if i < 4 - 1:
            g.write(" ")
    g.write("\n")

