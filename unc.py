f = open("MASTER_DATA.txt", "r")

MAX_REL_UNC = 0.0
bad_angle = 0
bad_unc = 0

for line in f:
    l = line.split()
    candidate = float(l[3]) / float(l[1])
    if candidate > MAX_REL_UNC:
        bad_angle, bad_unc = float(l[1]), float(l[3])
        MAX_REL_UNC = max(MAX_REL_UNC, float(l[3]) / float(l[1]))

print("DEBUG:", bad_angle, bad_unc)
print(MAX_REL_UNC)