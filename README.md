# VULCAN-Venus
#### Authors: Longkang Dai ####
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\
This is an open-access chemistry-transport model spanning both the middle and lower atmospheres on Venus, compiled by Python 3. 

The theory papers of VULCAN can be found here: Dai et al. (2024, accepted).

The framwork of this work is adopted from [VULCAN](https://github.com/exoclime/VULCAN) developed by [Tsai et al. (2017)](https://arxiv.org/abs/1607.00409). Thus, VULCAN-Venus has similar structure and operation method as VULCAN.


## Requirements
VULCAN-Venus is advised to run on Python 3.
Two very useful tools to set up python environments:\
[Pip](https://pip.pypa.io/en/stable/) - package installer for Python\
[Anaconda](https://docs.continuum.io/) - virtual environment manager

VULCAN requires the following python packages:
- numpy
- scipy
- Sympy
- matplotlib
- PIL/Pillow (optional: for interactive plotting)
- PyMieScatt (If the clouds are not released, this package is useless. Then, one should remove its import in op.py.)
- and the embeded [FastChem](https://github.com/exoclime/FastChem) requires a standard C++ compiler, like g++ or Clang.

If any of the python packages are missing, you can install the full SciPy Stack via Pip, e.g.
```bash
pip3 install --upgrade pip
```
```bash
pip3 install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
```
The above commands update pip and install SciPy via pip (use pip instead of pip3 if running with python2). Further information can be found at http://www.scipy.org/install.html

PIL or Pillow is a plotting library. If installed, the plots will be conveniently shown by the os-built-in image viewer. See https://github.com/python-pillow/Pillow for more information.  

## Quick Demo

First, go to the ```/fastchem_vulcan``` folder to compile [FastChem](https://github.com/exoclime/FastChem)(equilibrium chemistry code) by running
```
make
```

After compiling finished, go back to the main directory of VULCAN and run
```
python3 vulcan.py
```


After the run finished with a steady state, we can dirive the output file stored in ```/output``` by default. The common methods to read this output file are described in ```/output/reading_data.py```.

Now you may want to try a different T-P input, changing the elemental abundances or vertical mixing. All these settings are prescreibed in ```vulcan_cfg.py```. For example, find and edit
```python
atm_file = 'atm/atm_Venus_B+Dkzz.txt'
```
for a different vertical mixing (K<sub>zz</sub>) run. Set use_live_plot = True/False if you wish to switch on/off the real-time plotting. More detailed instruction can be found in the following sections. Have fun!

## Full instruction

### Structure
```
├── VULCAN/
│   ├── atm/
│   ├── fastchem_vulcan/
│   ├── output/
│   ├── plot/
│   ├── plot_py/
│   ├── /thermo/
│   │   ├──/NASA9/
│   │   ├──/Networks/
│   │   │   ├──/Nominal.txt
│   │   ├──/photo_cross/
│   │   ├── all_compose.txt
│   │   ├── gibbs_text.txt
│   ├── build_atm.py  
│   ├── chem_funs
│   ├── make_chem_funs.py
│   ├── modify_chem.py
│   ├── op.py
│   ├── phy_const.py
│   ├── store.py
│   ├── vulcan.py
│   ├── vulcan_cfg.py
```

`/atm/`: storing input atmospheric files
`/fastchem_vulcan/`: Fastchem (equilibirum chemistry code) which is used to initialse the compositions
`/output/`: storing the output files
`/plot/`: storing the output plots
`/thermo/`: storing chemical kinetics networks and thermodynamic data
`/thermo/NASA9/`: storing the NASA-9 polynomials for the Gibbs free energy of every species (We note that the rate coefficients of the reverse reactions are provided directly rather than calculated through the forward reactions in the nominal model. The values of the Gibbs free energy do not influence the results. 
`/thermo/Networks/`: storing the adopted chemical networks
`/thermo/photo_cross/`: storing the cross sections of the species
`/thermo/all_compose.txt`: basic compositional properties e.g. number of atoms and molecular weight
`/thermo/gibbs_text.txt`: a text file used by make_chem_funs.py to generate chem_funs.py
`build_atm.py`: modules to construct the atmospheric structure based on the input and to set up the initial compositions                
`chem_funs.py`: the functions of chemical sources/sinks, Jacobian matrix and the equilibrium constants     
`op.py`: all the modules for the numerical operations, e.g. computing reaction rates, ODE solvers etc.    
`make_chem_funs.py`: the routine that runs first to produce the required `chem_funs.py` based on the assigned chemical network    
`modify_chem.py`: additional operations on the reaction rates
`phy_const.py`: physical constants  
`store.py`: modules to store all the variables  
`vulcan.py`: the top-level main script of VULCAN  
`vulcan_cfg.py`: the configuration file for VULCAN  

Typically ```vulcan_cfg.py``` is the only file you need to edit for each specific run. If you want to look inside or modify the code, `store.py` is where almost all classes and variables are declared.  


### Configuration File ###
<strong>All the settings and parameters, e.g. the atmospheric parameters, the elemental abundance etc, are prescribed in ```vulcan_cfg.py```</strong>. Typically this is the only file you need to edit for each specific run. A useful cheatsheet describing what every parameter does can be found in ```vulcan_cfg_README.txt```.   

### Input Files
The key input files of VULCAN-Venus include the chemical network, atmospheric T-P-K<sub>zz</sub> profile, incident actinic flux. ```thermo/Networks/Nominal.txt``` is the deafult reaction network including nitrogen, carbon, hydrogen, oxygen, sulfur, and chlorine species. 
The rate coefficients A, B, C are written in A, B, C as in the Arrhenius formula k = A T^B exp(-C/T).
The input temperature-pressure-K<sub>zz</sub> profile is required when K<sub>zz</sub>_prof is set to 'file' in vulcan_cfg.py and is placed in the `/atm` folder by default. The first line in the T-P-K<sub>zz</sub> file is commented for units, and the second line must specifies the column names: **Pressure	Temp  	Kzz** (Kzz is optional). So the file consists of two columns without K<sub>zz</sub> and three columns with K<sub>zz</sub>.

The stellar UV flux is stored in /atm/stellar_flux, with the first column being weavelength in nm and the second column	being flux in ergs/cm**2/s/nm. If the use_sflux_top = True (in vulcan_cfg.py), the stellar UV flux will not be read, instead, the read one is stored in sflux_top_path as the incident flux at the top boundary.
The thermodynamics data and cross sections are stored in /thermo/NASA9 and /thermo/photo_cross, respectively. Change at your own risk! The thermodynamics data of several species lack experimental measurements like "ClCO3", we fill them with dummy ones to keep the code running stably. In this case, the inverse reactions is provided directly in VULCAN-Venus, and the auto-calculation of the inverse reactions from the forward ones by the thermodynamics data is switched off by remove_list = [i*2 for i in range(1,1000)] in vulcan_cfg.py. This means the thermodynamics data will not influence the nominal results. The model keeps the function of calculating reverse reactions in case of further modifications. 
If constant fluxes for certain species are used, the files are also placed in /atm, in the format of species, flux (cm-2 s-1), and deposite velocity (cm s-1).



### Editing or Using a different chemical network
VULCAN is developed in a flexible way that the chemical network is _not_ hard coded. Instead, ```make_chem_funs.py``` generates all the required funtions from the input chemical network into ```chem_funs.py```.
You can edit the default netowrk, to remove or add reactions, to change rate constats, etc. You can also use a different chemical network, as long as it is in the same format as the defalut ones. That is, the reactions should be writen in the form of [ A + B -> C + D ], including the square brackets.
By default, ```make_chem_funs.py``` is always called prior to the main code to produce ```chem_funs.py``` based on the new chemical network . This step (which takes a few seconds) can be skiped by adding the agument ```-n```while running vulcan in the command line:
```
python vulcan.py -n
```
However, it is important NOT to skipping this step after making a change of the chemical network.

If one needs to add to a reaction with complex rate coefficient expression, modify_chem.py is the place to have a further adjustment.

Noted that changing or using a different chemical network is not foolproof -- unrealistic values could lead to numerical issues. 

If one wants to switch on the calculation of reverse reactions from the forward ones, set remove_list = [] and remove all the reverse reactions in the network file. Be careful with those species lacking thermodynamics data or containing sulfur element. So next, make sure all the species are included in the ```NASA9``` folder. If not, they need to be added manually by looking over ```nasa9_2002_E.txt``` or ```new_nasa9.txt```, which can also be found in ```NASA9```. Save the coefficients in a text file with the same name as used in the network (e.g. CO2.txt). The format of the NASA 9 polynomials is as follows
```
a1 a2 a3 a4 a5
a6 a7 0. a8 a9
```
Here, a7 and a8 are separated by 0. The first two rows are for low temperature (200 - 1000 K) and the last two rows are for high temperature (1000 - 6000 K).\

The reaction number, i.e. **id**, is irrelevent as it will be automatically generated (and writing into the network file) while calling ```make_chem_funs```. Three-body or dissociation reactions should also be separately listed after the comment line as the default network.
After changing the network, you can examine all the readable information, like the list of reactions and species in ```chem_funs.py```, being updated while running python vulcan.py (without -n argument).

### Boundary Conditions ###
If both use_topflux and use_botflux in vulcan_cfg.py are set to False, it will use the default boundary condition -- zero flux boundary i.e. nothing coming in or out. When use_topflux = True, it reads the file prescribed in top_BC_flux_file as the incoming/outgoing flux at the top boundary. Similarly, when use_botflux = True, the file prescribed in bot_BC_flux_file is read in for the surface pressure and sinks at the bottom boundary. In addition, you can also use the dictionary use_fix_sp_bot to set fixed mole fraction at the surface. e.g. use_fix_sp_bot = {'CO2': 0.96} sets the surface CO<sub>2</sub> mixing ratio to 0.96.

### Reading Output Files 	###
The script of ```output/reading_data.py``` serve as a good example of how to access to output files. The first step is to use "pickle.load" to unpack the binary files. The main variables are stored in three basic classes: data['variable'], data['atm'], and data['parameter'].
You can also find all the names of variables and the class structure in ```store.py```.



## Remarks
The project receives financially support from the National Natural Science Foundation of China and Natural Science Foundation of Hunan Province, technical guidance from Shang-Min Tsai, Paul B. Rimmer and Carver J. Bierson.

VULCAN-Venus is publicly accessable. To use it, please cite Dai et al. (2024, accepted)
