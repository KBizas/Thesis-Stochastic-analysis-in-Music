import numpy as np
import scipy as sp

def scale_averages(k,move):
    return [np.mean(move[i:i+k]) for i in range(0, len(move), k)]

def var_estimator(moving_averages):
    meanie=np.mean(moving_averages)
    return sum( [ (element-meanie)**2 for element in moving_averages ] ) / (len(moving_averages) - 1 ) 

def h_define(k, h_estimates):
    kapa=range(len(h_estimates))
    slope, intercept, r_value, p_value, std_err = sp.stats.linregress(kapa,h_estimates)
    return (slope+2)/2

def conditionals(varest, HK):
    varcon = []
    epsilon = 1 / (1 - 2 ^ (2-2*HK))
    for k in range(0, len(varest)):
        varcon.append[epsilon*(varest[k]-varest[2*k])]
    return varcon

def m_define(varest):
    # kappa=range(k/2)
    # clim_spectum=[]
    # # for i in kappa:
    #     clim_spectum.append(i * (varest[i]-varest[2*i])/ np.log(2))
    # slope, intercept, r_value, p_value, std_err = sp.stats.linregress(kappa, clim_spectum)

    # k=len(varest)
    # clim = [k*( (varest[k]-varest[2*k])/ np.log(2) ) while k<len(varest)/2]
    M = 1 + np.log( (varest[0]-varest[1])/ np.log(2) )
    if M>1:
        M=0.9
    return M# , clim_spectum

def climacogram(k,varest):
    return k*( (varest[k]-varest[2*k])/ np.log(2) )

def log_climacogram(k,varest):
    return np.log( k*( (varest[k]-varest[2*k])/ np.log(2) ) )

def HK_base_theoretical(H, varest):
    var_0 = varest[0]
    var_theoretical=[]
    for k in range(1,len(varest)):
        var_theoretical.append(var_0/k**(2-2*H))
    bias=bias_define(varest, var_theoretical)
    var_theoretical = [var_theoretical[k]*bias for k in range(0, len(var_theoretical))]
    return var_theoretical

def bias_define(varest, var_theoretical):
    bias_coef=[np.mean(varest)/var_theoretical[k] for k in range(0,len(varest)-1)]
    return np.mean(bias_coef)


def FHKC(varest ,H ,M):
    var_0 = varest[0]
    FHKC_expo = (H-1) / M
    var_theoretical = [var_0*(1 + k**(2*M))**FHKC_expo for k in range(1,len(varest))]
    bias=bias_define(varest, var_theoretical)
    var_theoretical = [var_theoretical[k]*bias for k in range(0, len(var_theoretical))]
    return var_theoretical

def FHKCperiodic(varest ,H ,M):
    kurt=np.var(varest)
    var_0 = varest[0]
    FHKC_expo = (H-1) / M
    var_theoretical = [var_0*(1 + k**(2*M))**FHKC_expo + kurt*np.sin( 16 * k ) for k in range(1,len(varest))]   #### to 16 einai to plh8os notwn ana metro dld ari8mhths metrou epi 2 san proseggush
    return var_theoretical


############# JUICE #########################

def GHK(k, H, M, a, var_0):
    return var_0 * ( (1 + k/a)**(2*M) ) ** ( (H-1) / M )

def log_GHK(k, H, M, a, var_0):
    return np.log( GHK(k, H, M, a, var_0) )

def GHK_M_fit(k, varest):
    k = range(len(varest))
    popt, pcov = sp.optimize.curve_fit( GHK, k, varest, p0=[0.5, 0.5, 1, varest[0]],
                                        bounds=([0.1, 0, 0.01, varest[0]*0.95], [1, 1, 64, varest[0]*1.05]))
    return popt

def refine_GHK(k, varest):
    k = range(len(varest))
    # M_spectrum = m_define(varest)
    H_drop, M_fitted, a_drop, var_0_drop = GHK_M_fit(k, varest)
    popt, pcov = sp.optimize.curve_fit( log_GHK, k, np.log(varest), p0=[0.5, M_fitted, 1, varest[0]],
                                        bounds=([0.1, 0.5*M_fitted, 0.01, varest[0]*0.95], [1, 1, 64, varest[0]*1.05]))
    if popt[1]>1:
        popt[1]=M_fitted
    return popt