* Ideal RC transient for HSPICE execution validation; no transistor PDK.
V1 in 0 PULSE(0 1 0 10p 10p 1n 2n)
R1 in out 1k
C1 out 0 1p
.tran 10p 5n
.print tran v(in) v(out)
.end
