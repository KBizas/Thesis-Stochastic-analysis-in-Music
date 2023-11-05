from model_calc import  scale_averages, var_estimator, GHK, refine_GHK #  h_define, m_define, HK_base_theoretical, FHKC,
from termcolor import colored
import matplotlib.pyplot as plt
from diabasma import  take_input_from_folder #take_input_from_user,
import numpy as np
from scipy.stats import skew
import os


def execute_thesis(data, temp):
    maintrack = data.data
    folder_name = data.folder_name
    file_name = data.file_name[:-4]
    k = maintrack.k
    moves = maintrack.notes


    k_scale_averages= [ scale_averages(i,moves) for i in range(1,k) ]
    varest = [var_estimator(k_average) for k_average in k_scale_averages]
    H, M, a, var_0 = refine_GHK(k, varest)
    var_theoretical = [GHK(i, H, M, a, var_0) for i in range(k)]
    # HK = h_define(k, varest)
    # clm_spectrum, M = m_define(k, varest)
    # var_theory_unbiased_HK = HK_base_theoretical(HK, varest)
    # var_theory_unbiased_FHK = FHKC(varest ,HK ,M)
    # bias = bias_define(HK, varest, len(moves))



    strig='C:/Users/user/Desktop/bigg/data/output/' +folder_name + '/' + file_name
    try:
        os.mkdir(strig)   
    except FileExistsError:
        pass


    print(H)
    print(M)

    plt.style.use('seaborn-v0_8-whitegrid')
    ax=plt.subplot()
    plt.hist(maintrack.move, color='green', bins=49)
    plt.title('distribution')
    plt.savefig(strig + '/distribution')                                                 ##### diafwnei to numpy me to plot
    plt.close()
    
    ax=plt.subplot()
    plt.plot(maintrack.notes, color='green')
    plt.title('pure time series')
    plt.savefig(strig + '/pure_time_series') 
    plt.close()

    fig, ax = plt.subplots()
    plt.xscale('log')
    plt.yscale('log')
    plt.title('climacogramm')
    plt.xlabel("k scale")
    plt.ylabel("k scale variance")
    ax.plot(varest, '-', color='cyan')
    ax.plot(var_theoretical, '-', color='crimson')
    plt.legend(["empirical", "FHKC"], loc="lower left")
    plt.savefig(strig + '/climacogramm') 
    plt.close()

    # fig, ax = plt.subplots()
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.title('climaco-spectrum')
    # plt.xlabel("k scale")
    # plt.ylabel("k scale variance")
    # ax.plot(clm_spectrum, '_', color='green')
    # plt.savefig(strig + '/climacospectrum') 
    # plt.close()

    if temp <= 9:
        name_counter = '00' +str(temp)
    elif temp <=99:
        name_counter = '0' + str(temp)
    else: name_counter = str(temp)

    # fp= open('C:/Users/user/Desktop/bigg/RESULTS/' + name_counter + file_name + '.csv', 'w')
    # fp.write(str(H) + '\n')
    # fp.write(str(M) + '\n')
    # fp.write(str(a) + '\n')
    # fp.write(str(var_0) + '\n')
    # fp.write(str(len(moves)) + '\n')
    # fp.write(str(folder_name) + '\n')
    # for i in var_theoretical:
    #     fp.write(str(i) + '\n')
    # fp.close

    first = np.mean(moves)
    second = np.var(moves)
    third = skew(moves)

    fp= open('C:/Users/user/Desktop/bigg/RevisedNoteStats/HurstR.txt', 'a')
    fp.write(str(H) + '\n')
    fp.close

    fp= open('C:/Users/user/Desktop/bigg/RevisedNoteStats/MparameterR.txt', 'a')
    fp.write(str(M) + '\n')
    fp.close

    fp= open('C:/Users/user/Desktop/bigg/RevisedNoteStats/a_stepR.txt', 'a')
    fp.write(str(a) + '\n')
    fp.close

    fp= open('C:/Users/user/Desktop/bigg/RevisedNoteStats/meanR.txt', 'a')
    fp.write(str(first) + '\n')
    fp.close

    fp= open('C:/Users/user/Desktop/bigg/RevisedNoteStats/varR.txt', 'a')
    fp.write(str(second) + '\n')
    fp.close

    fp= open('C:/Users/user/Desktop/bigg/RevisedNoteStats/skewR.txt', 'a')
    fp.write(str(third) + '\n')
    fp.close

    fp= open('C:/Users/user/Desktop/bigg/RevisedNoteStats/variabilitycoef.txt', 'a')
    fp.write(str(first / np.sqrt(second)) + '\n')
    fp.close

# maintrack = take_input_from_user()
# execute_thesis(maintrack)

data = take_input_from_folder()
temp=1
for dato in data:
    execute_thesis(dato, temp)
    temp=temp+1