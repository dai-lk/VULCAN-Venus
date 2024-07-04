# ============================================================================= 
# Configuration file of VULCAN:  
# ============================================================================= 

# ====== Setting up altitude and density array =========
alt_path = 'atm/alt_venus.txt'
# ====== fix sp from the begining (do not related to condensation) =====
#fix_sp_start = ['H2SO4', 'H2O', 'H2O_l_s', 'H2SO4_l', 'V', 'V2']
# ====== cloud particle and UV absorber =======
N_particle_path = 'atm/mode1+2.txt'
UV_absorber_path = 'atm/UV_absorber.txt'
# ====== Setting up the elements included in the network ======
atom_list = ['S','N','C','H','O','Cl','V']

# ====== Setting up paths and filenames for the input and output files  ======
# input:
network = 'thermo/Networks/Nominal.txt' # Chemical network in nominal and Model A
use_lowT_limit_rates = False
gibbs_text = 'thermo/gibbs_text.txt' # (all the nasa9 files must be placed in the folder: thermo/NASA9/)
cross_folder = 'thermo/photo_cross/'
com_file = 'thermo/all_compose.txt'
atm_file = 'atm/atm_Venus_Bkzz.txt' # TP and Kzz (optional) file, Kzz from Bierson & Zhang 2020
#atm_file = 'atm/atm_Venus_B+Dkzz.txt' # Kzz from Bierson & Zhang 2020 + Dai 2023
sflux_file = 'atm/stellar_flux/Gueymard_solar.txt' # Only used when use_sflux_top = False. This is the flux density at the stellar surface
top_BC_flux_file = 'atm/BC_top_Venus.txt' # the file for the top boundary conditions
bot_BC_flux_file = 'atm/BC_bot_Venus.txt' # the file for the lower boundary conditions
#vul_ini = 'atm/ini_atm_Venus.txt' # the file to initialize the abundances
vul_ini = 'output/Nominal_Bkzz_SO2.vul'
# output:
output_dir = 'output/'
plot_dir = 'plot/'
movie_dir = 'plot/movie/'
out_name =  'Nominal_Bkzz_SO2.vul' # output file name: Nominal_Bkzz_SO2, A_Dkzz_SO2

# ====== Setting up the elemental abundance ======
use_solar = True # True: using the solar abundance from Table 10. K.Lodders 2009; False: using the customized elemental abundance. 
# customized elemental abundance (only read when use_solar = False)
O_H = 6.0618E-4 *(0.85) #*(0.793)  
C_H = 2.7761E-4  
N_H = 8.1853E-5
S_H = 1.3183E-5
He_H = 0.09692
ini_mix = 'vulcan_ini' # Options: 'EQ', 'const_mix', 'vulcan_ini', 'table' (for 'vulcan_ini, the T-P grids have to be exactly the same)

# Initialsing uniform (constant with pressure) mixing ratios (only reads when ini_mix = const_mix)
const_mix = {'CO2':0.96, 'N2':0.03, 'SO2':1.5E-4,  'H2O':3.5E-5, 'CO':2E-5, 'COS': 5E-6,'HCl':4E-7} 

# ====== Setting up photochemistry ======
use_photo = True
use_sflux_top = True # Longkang added for setting directly the actinic flux at the top of planetary atmosphere
sflux_top_path = 'atm/stellar_flux/Venus_topsflux_Xiz2012.txt' # Longkang added, only used if use_sflux_top = True
# astronomy input
r_star = 1 # stellar radius in solar radius
Rp = 6.0518e8 # Planetary radius (cm) (for computing gravity)
orbit_radius = 0.72 # planet-star distance in A.U.
sl_angle = 58 /180.*3.14159 # the zenith angle of the star in degree (usually 58 deg for the dayside average)
f_diurnal = 0.5 # to account for the diurnal average of solar flux (i.e. 0.5 for Earth; 1 for tidally-locked planets) 
scat_sp = ['CO2','N2','H2','O2'] # the bulk gases that contribute to Rayleigh scattering
T_cross_sp = ['H2O2','CO2','H2O'] # warning: slower start! available atm: 'CO2','H2O','NH3', 'SH','H2S','SO2', 'S2', 'COS', 'CS2'

edd = 0.5 # the Eddington coefficient 
dbin1 = 0.1  # the uniform bin width < dbin_12trans (nm)
dbin2 = 2.   # the uniform bin width > dbin_12trans (nm)
dbin_12trans = 240. # the wavelength switching from dbin1 to dbin2 (nm)

# the frequency to update the actinic flux and optical depth
ini_update_photo_frq = 100
final_update_photo_frq = 5

# ====== Setting up ionchemistry ======
use_ion = False
if use_photo == False and use_ion == True:
    print ('Warning: use_ion = True but use_photo = False')
# photoionization needs to run together with photochemistry


# ====== Setting up parameters for the atmosphere ======
atm_base = 'CO2' #Options: 'H2', 'N2', 'O2', 'CO2 -- the bulk gas of the atmosphere: changes the molecular diffsion, thermal diffusion factor, and settling velocity
rocky = True # for the surface gravity
nz = 57   # number of vertical layers
P_b = 9.208E7  # pressure at the bottom (dyne/cm^2)
P_t = 1.159 # pressure at the top (dyne/cm^2)
use_Kzz = True
use_moldiff = False
use_vz = False
atm_type = 'file'  # Options: 'isothermal', 'analytical', 'file', or 'vulcan_ini' 'table'
Kzz_prof = 'file' # Options: 'const','file' or 'Pfunc' (Kzz increased with P^-0.4)
K_max = 1e5        # for Kzz_prof = 'Pfunc'
K_p_lev = 0.1      # for Kzz_prof = 'Pfunc'
vz_prof = 'const'  # Options: 'const' or 'file'
gs = 870.         # surface gravity (cm/s^2)  (HD189:2140  HD209:936)
Tiso = 1000 # only read when atm_type = 'isothermal'
# setting the parameters for the analytical T-P from (126)in Heng et al. 2014. Only reads when atm_type = 'analytical' 
# T_int, T_irr, ka_L, ka_S, beta_S, beta_L
para_warm = [120., 1500., 0.1, 0.02, 1., 1.]
para_anaTP = para_warm
const_Kzz = 1.E10 # (cm^2/s) Only reads when use_Kzz = True and Kzz_prof = 'const'
const_vz = 0 # (cm/s) Only reads when use_vz = True and vz_prof = 'const'

# frequency for updating dz and dzi due to change of mu
update_frq = 100 

# ====== Setting up the boundary conditions ======
# Boundary Conditions:
use_topflux = True
use_botflux = False
use_fix_sp_bot = {'NO':5.5E-9, 'CO2':0.965, 'CO':1.5E-5, 'SO2':1.E-4, 'COS':3E-5, 'HCl':4E-7, 'H2':1E-5, 'H2S':1E-8} #fixed mixing ratios at the lower boundary
diff_esc = [] # species for diffusion-limit escape at TOA
max_flux = 1e20  # upper limit for the diffusion-limit fluxes

# ====== Reactions to be switched off  ======
remove_list = [i*2 for i in range(1,1000)] # We stop the auto-calculation of the reverse reactions and provide them directly @Longkang

# == Condensation ======
use_condense = True
use_settling = False
use_relax = ['H2O', 'H2SO4']
humidity = 0.25 # only for water
r_p = {'H2O_l_s': 0.01, 'H2SO4_l': 1e-4}  # particle radius in cm (1e-4 = 1 micron)
rho_p = {'H2O_l_s': 0.9, 'H2SO4_l': 1.8302} # particle density in g cm^-3
start_conden_time = 0
condense_sp = ["H2O" , "H2SO4"]      
non_gas_sp = [ 'H2O_l_s', "H2SO4_l"]
fix_species = ['H2SO4', 'H2O', 'H2O_l_s', 'H2SO4_l', 'V', 'V2','N2']   # fixed the condensable species after condensation-evapoation EQ has reached
fix_species_time = 1.E-20 # after this time to fix the condensable species, this part should be re-built if the cloud is released @Longkang

# ====== steady state check ======
st_factor = 0.5
conv_step = 50

# ====== Setting up numerical parameters for the ODE solver ====== 
ode_solver = 'Ros2' # case sensitive
use_print_prog = True
use_print_delta = True
print_prog_num = 500  # print the progress every x steps
dttry = 1.E-13
trun_min = 1e2
runtime = 1.E22
dt_min = 1.E-14
dt_max = runtime*1e-5
dt_var_max = 2
dt_var_min = 0.5
count_min = 120
count_max = int(1E5)
# atol: if dy < atol: then treat dy = 0
atol = 1E-3 # Try decreasing this if the solutions are not stable
# mtol: if dymix < mtol: then treat dymix = 0
mtol = 1.E-22
mtol_conv = 1.E-16
pos_cut = 0
nega_cut = -1.
loss_eps = 1e12 # for using BC
yconv_cri = 0.01 # the largest percentage of the ymix variation for checking steady-state
slope_cri = 1.e-5 # the largest mean percentage of the varying ymix in uint time for checking steady-state
yconv_min = yconv_cri # the largest percentage of the ymix variation for checking steady-state
flux_cri = 0.1 # the absolute tolerence for actinc flux (# photons cm-2 s-1 nm-1)
flux_atol = 1. # the thershold of change of actinic flux for checking steady-state

# test one step
'''ini_update_photo_frq = 5
final_update_photo_frq = 5
dt_max = 1E-12
count_min = 1
count_max = int(3)'''

# ====== Setting up numerical parameters for Ros2 ODE solver ====== 
rtol = 0.02              # relative tolerence for adjusting he stepsize
post_conden_rtol = 0.02 # switched to this value after fix_species_time

# ====== Setting up for ouwtput and plotting ======
# plotting:
plot_TP = False
use_live_plot = False
use_live_flux = False
use_plot_end = False
use_plot_evo = False
use_save_movie = False
use_flux_movie = False
plot_height = False
use_PIL = True 
live_plot_frq = 10
save_movie_rate = live_plot_frq
y_time_freq = 1  #  storing data for every 'y_time_freq' step
plot_spec = ['H2O', 'H2O_l_s','H2SO4','H2SO4_l','SO2', 'SO','CO']  
# output:
output_humanread = False
use_shark = False
save_evolution = False   # save the evolution of chemistry (y_time and t_time) for every save_evo_frq step
save_evo_frq = 10
