# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 19:32:59 2021

@author: victo
"""

    # Create associated plot
    fig, axs = plt.subplots(1, 3,figsize=[11, 6],sharey=True,dpi=100)
    axs[0].errorbar(x=list(nd1),y=list(altitude_grid),xerr=list(nd1_err),capsize=0,elinewidth=1,ecolor='red',marker='o',markerfacecolor='red',markersize=2,ls='-',color='red')
    axs[0].errorbar(x=list(nd2),y=list(altitude_grid),xerr=list(nd2_err),capsize=0,elinewidth=1,ecolor='forestgreen',marker='o',markerfacecolor='forestgreen',markersize=2,ls='-',color='forestgreen')             
    title = 'Average O3 Volume Mixing Ratio' 
    axs[0].set_title(title)
    axs[0].set_ylim(0,105)
    axs[0].set_xlim(-1e-7,1e-4)
    axs[0].set_xlabel('Average VMR [molec cm^-3]',labelpad=18)
    axs[0].set_ylabel('Altitude [km]') 
    # for i in range(0,100,6):
    #    if N1[i]!=0:
    #       axs[0].annotate( N1[i], xy=(nd1[i], altitude_grid[i]), xytext=(1.0*10**13,altitude_grid[i]))
    x=[0,0] # Set up two points for a dark line to show the ideal 0 point.
    y=[0,155]  
    axs[1].plot(numpy.concatenate([numpy.array(diff) + numpy.array(diff_stddev), numpy.array(diff) - numpy.array(diff_stddev)]),list(altitude_grid)+list(altitude_grid),'--',color='dimgrey',label='Mean \u0394 ± \u03C3')
    axs[1].errorbar(x=list(diff),y=list(altitude_grid),xerr=list(diff_err),marker='o',capsize=0,elinewidth=1,ecolor='deeppink',markerfacecolor='deeppink',markersize=0,color='deeppink',label='Mean \u0394',linewidth=1)   
    axs[1].legend(['Mean \u0394', 'Mean \u0394 ± \u03C3'], bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=1, borderaxespad=1.0)
    title = 'Mean Absolute Differences ' 
    axs[1].set_title(title)
    axs[1].set_xlim(-3e-3,1e-3)
    axs[1].set_ylim(0,105)
    axs[1].set_xlabel('Difference [molec cm^-3]',labelpad=18)
    axs[1].plot(x,y,color='black') # Ideal 0 line.
    axs[2].plot(x,y,color='black') # Ideal 0 line.    
    axs[2].plot(numpy.concatenate([numpy.array(rel_diff) + numpy.array(rel_diff_stddev),numpy.array(rel_diff) - numpy.array(rel_diff_stddev)]),list(altitude_grid)+list(altitude_grid),'--',color='dimgrey',linewidth=1)
    axs[2].errorbar(x=list(rel_diff),y=list(altitude_grid),xerr=list(rel_diff_err),marker='o',capsize=0,elinewidth=1,ecolor='deeppink',markerfacecolor='deeppink',markersize=0,color='deeppink',linewidth=2)
    title = 'Mean Relative Differences ' 
    axs[2].set_title(title)
    axs[2].set_ylim(0,105)
    axs[2].set_xlim(-100,100)
    axs[2].set_xlabel('Difference [%]',labelpad=18)
    filenamepng = title + ' ACE-MAESTRO UV & VIS, errorbars.png' # Create name for png plot file.
    fig.savefig(filenamepng) 
    