##*PAN*##

PAN is the MoM (metchod of moment) Electromagnetic Numerical code for simlating planar antnena structure.  The code is still under development but can simulate many planar structures already.  Here is a list of features to develop.
1. GUI
2. Add transmit alrorithm
3. Add current flow chart

**Prerequisite:**

1. Python 2.7.x

2. pydistmesh

3. matplotlib 1.4.x

4. numpy


**Usage:**

1. Retrieve git repository.
```
git clone https://github.com/antopenrf/mom.git
```

2. Start the demos.
```
>cd PAN
>python demo_dipole.py
.
.
>TRP = 0.00866872915467 Watt, D = 1.61421250962, 2.07960708626 dB
>python demo_plot.py

```

**Examples:**
For simulating the dual stubs, use poly moudle to create the polygon as shown in demo_dualstubs.py.

```
>python demo_dualstubs.py
>python demo_plot.py
```

1.Mesh

![mesh](/results/dual_stub_mesh.png)

2.Current Density

![current densities](/results/dual_stub_densities.png)


3.2D cuts

-xy
![xy 2D cut](/results/dual_stub_xy.png)

-yz
![yz 2D cut](/results/dual_stub_yz.png)

-zx
![zx 2D cut](/results/dual_stub_zx.png)

