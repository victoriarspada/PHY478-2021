# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 12:05:43 2021

@author: victo
"""

years = [2004,2005,2006,2007,2008,2010,2011]

for year in years:
    name = 'acemaestro_uvvis_'+str(year)+'_vis_info_arrays.pickle'
    pickle_in = open(name,"rb")
    open_meas = pickle.load(pickle_in) #Open the pickle file
    o3_vmr_vis = open_meas['o3_vmr']
    o3_vmr_error_vis = open_meas['o3_vmr_error']
    retrievals_vis = open_meas['retrievals']
    dates_vis = open_meas['dates']
    longitudes_vis = open_meas['longitudes']
    latitudes_vis = open_meas['latitudes']
    pickle_in.close()

    name = name = 'acemaestro_uvvis_'+str(year)+'_uv_info_arrays.pickle'
    pickle_in = open(name,"rb")
    open_meas = pickle.load(pickle_in) #Open the pickle file
    o3_vmr_uv = open_meas['o3_vmr']
    o3_vmr_error_uv= open_meas['o3_vmr_error']
    retrievals_uv = open_meas['retrievals']
    dates_uv = open_meas['dates']
    longitudes_uv = open_meas['longitudes']
    latitudes_uv = open_meas['latitudes']
    pickle_in.close()

    dates_uv_num, dates_vis_num = [], []

    for elem in dates_uv:
        dates_uv_num = dates_uv_num + [plt.date2num(elem)]
    for elem in dates_vis:
        dates_vis_num = dates_vis_num + [plt.date2num(elem)]

    name = 'acemaestro_uvvis_'+str(year)+'_vis_info_arrays.pickle'
    a = {'o3_vmr' : o3_vmr_vis,
         'o3_vmr_error' : o3_vmr_error_vis,
         'retrievals' : retrievals_vis,
         'longitudes' : longitude_vis,
         'latitudes' : latitude_vis,
         'dates' : dates_vis
         'datenumbers': dates_vis_num}
    pickle_out = open(name,"wb")
    pickle.dump(a, pickle_out)
    pickle_out.close()

    name = 'acemaestro_uvvis_'+str(year)+'_uv_info_arrays.pickle'
    a = {'o3_vmr' : o3_vmr_uv,
         'o3_vmr_error' : o3_vmr_error_uv,
         'retrievals' : retrievals_uv,
         'longitudes' : longitude_uv,
         'latitudes' : latitude_uv,
         'dates' : dates_uv
         'datenumbers': dates_uv_num}
    pickle_out = open(name,"wb")
    pickle.dump(a, pickle_out)
pickle_out.close()