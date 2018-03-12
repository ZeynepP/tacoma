import matplotlib.pyplot as pl
from matplotlib.collections import LineCollection
import networkx as nx
import numpy as np

from scipy.optimize import curve_fit

import tacoma as tc

from rocsNWL.drawing import draw
from rocsNWL.drawing import get_pos

_layout_function = 'graphviz'

def draw_edge_lists(L):

    G = nx.Graph()
    G.add_nodes_from(range(L.N))
    G.add_edges_from(L.edges[0])
    
    pos, _ = get_pos(G,layout_function=_layout_function)

    fig,ax = pl.subplots(1,len(L.edges),figsize=(len(L.edges)*3,4))
    ax = ax.flatten()

    draw(G,pos=pos,ax=ax[0],layout_function=_layout_function)

    for i in range(1,L.N):
        G = nx.Graph()
        G.add_nodes_from(range(L.N))
        G.add_edges_from(L.edges[i])
        
        draw(G,pos=pos,ax=ax[i],layout_function=_layout_function)

def draw_edges(traj,
               time_normalization_factor = 1.,
               time_unit = None,
               fit = False,
               ):

    fig, ax = pl.subplots(1,1)
    lines = []
    max_i = len(traj)
    all_t_max = []
    all_t_min = []
    max_node = []
    for i, entry in enumerate(traj):
        all_t_max.append(entry.time_pairs[-1][-1] * time_normalization_factor)
        all_t_min.append(entry.time_pairs[0][0] * time_normalization_factor)
        max_node.extend(entry.edge)
        for t_ in entry.time_pairs:
            t_ = np.array(t_) * time_normalization_factor
            lines.append([ t_, [i,i]])

    fit_x = np.array(all_t_min)
    fit_y = np.arange(len(traj),dtype=float)
    

    lines = [zip(x, y) for x, y in lines]

    ax.add_collection(LineCollection(lines))

    t0 = min(all_t_min)
    ax.set_ylim(-1,max_i)
    ax.set_xlim(t0,max(all_t_max))

    xlabel = 'time'
    if time_unit is not None:
        xlabel += ' ['+time_unit+']'

    ylabel = 'edge id'
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if fit:
        N = max(max_node) + 1
        fac = N*(N-1)/2.
        fit = lambda x, alpha, fac: fac * (1 - np.exp(-alpha*(x-t0)))
        popt, pcov = curve_fit(fit, fit_x, fit_y,[1./fac,fac],maxfev=10000)

        ax.plot(fit_x, fit(fit_x,*popt),'r')


    return fig, ax

if __name__ == "__main__":
    import time

    L = tc.edge_lists()

    L.N = 3
    L.t = [0.0,1.0,2.0]
    L.tmax = 3.0
    L.edges = [ 
                [
                  (0,1)
                ],
                [
                  (1,2), (0,2)
                ],
                [
                  (0,1)
                ],
               ]

    L = tc.dynamic_RGG(100,100,mean_link_duration = 10)
    #F = tc.flockwork_P_varying_rates([],100,[0.5],100,[(0.0,1.0)],tmax=100)
    F = L
    FBIN = tc.bin(F,dt=1)
    #draw_rows(FBIN)

    start = time.time()
    result = tc.get_edge_trajectories(FBIN)
    end = time.time()
    traj = result.trajectories
    print result.edge_similarities

    print "needed ", end-start, "seconds"
    draw_edges(traj,fit=True)

    start = time.time()
    result = tc.get_edge_trajectories(F)
    end = time.time()
    traj = result.trajectories
    print "needed ", end-start, "seconds"
    draw_edges(traj)



    #draw_edge_lists(L)

    pl.show()