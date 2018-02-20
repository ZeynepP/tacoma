import cFlockwork as cF

sample_aggregates = True
N_time_steps = 5

print "===== edge_lists => edge_lists ====="

L = cF.edge_lists()

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


new = cF.resample_from_edge_lists(L,N_time_steps=N_time_steps,sample_aggregates=sample_aggregates,verbose=True)

print new.N
print new.t
print new.tmax
print new.edges


print "===== edge_changes => edge_lists ====="

C = cF.edge_changes()

C.N = 3
C.edges_initial = [ (0,1) ]
C.t0 = 0.0
C.tmax = 3.0
C.t = [ 1.0, 2.0 ]
C.edges_in = [
                [
                    (1,2), (0,2)
                ],
                [
                    (0,1),
                ],
             ]
C.edges_out = [
                [
                    (0,1)
                ],
                [
                    (1,2), (0,2)
                ],
              ]

new = cF.resample_from_edge_changes(C,N_time_steps=N_time_steps,sample_aggregates=sample_aggregates,verbose=True)

print new.N
print new.t
print new.tmax
print new.edges

