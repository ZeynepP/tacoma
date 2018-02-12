import cFlockwork as cF
import matplotlib.pyplot as pl
from collections import Counter
from itertools import izip
import numpy as np

def get_hist_from_counter(c):

    data = np.array(c.items(),dtype=float)

    x = data[:,0]
    y = data[:,1] / data[:,1].sum()

    return x,y

N = 100

print "simulating"
result = cF.ZSBB_model([],N,1.0,0.7,0.7,1000000,seed=1346,record_sizes_and_durations=True)
print "done"

fig, ax = pl.subplots(1,3,figsize=(12,4))

x,y = get_hist_from_counter(Counter(result.durations))
ax[1].plot(x,y,'s')
ax[1].set_yscale('log')
ax[1].set_xscale('log')

size_count = Counter()
size_count[1] = N
this_count = Counter(size_count)

m_edges = 0
ks = []
print len(result.edges_in[0])
print result.edges_in[0]
edges_in = result.edges_in
edges_out = result.edges_out
for ch,e_in,e_out in izip(result.group_changes,edges_in,edges_out):
    #print ch, e_in, e_out
    this_count += Counter(ch)
    size_count += this_count
    m_in = len(e_in)
    m_out = len(e_out)
    m_edges += m_in
    m_edges -= m_out
    mean_k = m_edges / (2.*N)
    ks.append(mean_k)


t = np.array(result.t,dtype=float)
t /= N

new_t = t[::N]
new_k = ks[::N]

print len(ks), len(result.t)






x,y = get_hist_from_counter(size_count)
ax[0].plot(x,y,'s')
ax[0].set_yscale('log')
ax[0].set_xscale('log')


ax[2].plot(new_t,new_k,'-')




pl.show()