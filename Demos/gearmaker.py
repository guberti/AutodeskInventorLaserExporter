import sys
# Makes TETRIX MAX gear specs
if len(sys.argv) != 2:
	print "Usage: gearmaker.py [tooth number]"

N = int(sys.argv[1])
DP = 32 # Diametrical pitch
print "Diametrical pitch: " + str(DP)
print "Outer diameter: " + str((N+2)/float(DP))
PD = N/float(DP)
print "Pitch diameter: " + str(PD)
print "Root diameter: " + str((N-2)/float(DP))

print "Quater angular circle pitch: " + str((90.0)/float(N))
print "Pitch point diameter circle:" + str(float(PD)/4.0)
