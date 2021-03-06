##*PAN*##

PAN is the MoM (method of moment) Electromagnetic Numerical code for simulating planar antenna structure.  The code is still under development but can simulate many planar structures already.  Here is a list of features to develop.
1. GUI
2. Add transmit algorithm
3. Add current flow chart

**Prerequisite:**

1. Python 2.7.x

2. pydistmesh

3. matplotlib 1.4.x

4. numpy

5. pyhull

**Usage:**

1. Retrieve git repository.
```
git clone https://github.com/antopenrf/pan.git
```

2. Start the demo for half-wavelength dipole.  The simulated directivity is 2.08 dB, close to the theoretical number, 2.15dB.
```
>cd PAN
>python demo_dipole.py
.
.
>TRP = 0.00866872915467 Watt, D = 1.61421250962, 2.07960708626 dB 
>python demo_plot.py
Select mesh to plot: (1)dipole (2)dual stubs (3)patch
1
```

**Examples:**
For simulating the dual stubs, use poly module to create the polygon as shown in demo_dualstubs.py.

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

