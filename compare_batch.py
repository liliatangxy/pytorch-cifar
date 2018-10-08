from __future__ import division
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
import math

tag = sys.argv[1]
batch_no = ["8", "16", "32", "64", "128"]

fwd_avgs = []
fwd_err = []
fwd_totals = []
back_avgs = []
back_err = []
back_totals = []

for j in range(len(batch_no)):
    fwd_n = 0
    fwd_total = 0
    fwd_var = 0
    back_n = 0
    back_total = 0
    back_var = 0
    with open("log/"+tag+'-'+batch_no[j]) as f:
        for l in f:
            p = l.split()
            if len(p) > 0:
                if p[0] == "Forward":
                    fwd = float(p[2])
                    fwd_n += 1
                    fwd_total += fwd
                    fwd_avg = fwd / fwd_n
                    if fwd_n > 1:
                        fwd_avg = fwd / fwd_n
                        dif = fwd - fwd_avg
                        fwd_var = fwd_var*(fwd_n-2)/(fwd_n-1) + dif*dif/fwd_n
                if p[0] == "Backward":
                    back = float(p[2])
                    back_n += 1
                    back_total += back
                    back_avg = back / back_n
                    if back_n > 1:
                        dif = back - back_avg
                        back_var = back_var*(back_n-2)/(back_n-1) + dif*dif/back_n
    fwd_totals.append(fwd_total)
    fwd_err.append(math.sqrt(fwd_var*fwd_n)*2)
    back_totals.append(back_total)
    back_err.append(math.sqrt(back_var*back_n)*2)

width = 0.35
idx = range(len(batch_no))

print fwd_err, back_err
p1 = plt.bar(idx, fwd_totals, width, yerr=fwd_err)
p2 = plt.bar(idx, back_totals, width, bottom=fwd_totals, yerr=back_err)
plt.ylabel('Time')
plt.title(tag + ' Time for Foward and Backward Propagation over Batch Sizes')
plt.xticks(idx, batch_no)
plt.legend((p1[0], p2[0]), ('Forward', 'Backward'))
plt.savefig("log/"+tag+"-time.pdf")
