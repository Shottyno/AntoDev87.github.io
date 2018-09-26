from __future__ import print_function

from netCDF4 import Dataset
from wrf import getvar, ALL_TIMES, get_basemap, latlon_coords, geo_bounds, to_np, get_cartopy, destagger, ll_to_xy
import numpy as np
from scipy.interpolate import griddata
from scipy import spatial
import pprint
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import ticker, cm
import matplotlib.colors
import json
import os

#26_09_2018_01:00

url = "http://193.205.230.6:8080/opendap/opendap/wrf5/d03/20180926Z00/wrfout_d03_2018-09-26_01:00:00.nc"

splitted = url.split("/")

#arr_data_ora = splitted[9].replace("%3A", ":").split("_")

arr_data_ora = splitted[8].split("_")

data_ora = arr_data_ora[2]+" "+arr_data_ora[3].replace(".nc", "")

#ncfile = Dataset("http://193.205.230.6:8080/opendap/opendap/wrf5/d03/20180702Z00/wrfout_d03_2018-07-06_00%3A00%3A00.nc")
ncfile = Dataset("http://193.205.230.6:8080/opendap/opendap/wrf5/d03/20180926Z00/wrfout_d03_2018-09-26_01:00:00.nc")
#ncfile = Dataset("http://193.205.230.6:8080/opendap/opendap/wrf5/d02/20180703Z00/wrfout_d02_2018-07-06_00%3A00%3A00.nc")

Xlat = getvar(ncfile, "XLAT", timeidx=ALL_TIMES)

Xlon = getvar(ncfile, "XLONG", timeidx=ALL_TIMES)

row_lat = len(Xlat) - 1 

col_lat = len(Xlat[0]) - 1

row_long = len(Xlon) - 1 

col_long = len(Xlon[0]) - 1

# Trovo il punto A [Xlat[0][0], Xlon[0][0]]

A = [Xlat[0][0], Xlon[0][0]]

# Trovo il punto B [Xlat[0][col_lat], Xlon[0][col_long]]

B = [Xlat[0][col_lat], Xlon[0][col_long]]

# Trovo il punto C [Xlat[row_lat][col_lat], Xlon[row_long][col_long]]

C = [Xlat[row_lat][col_lat], Xlon[row_long][col_long]]

# Trovo il punto D [Xlat[row_lat][0], Xlon[row_long][0]]

D = [Xlat[row_lat][0], Xlon[row_long][0]]

min_lat = Xlat[0][0]

minI = 0

Xlat[0][0] - Xlat[1][1]

Xlon[0][0] - Xlon[1][1]

''' from A to B '''
for i in xrange(col_lat,-1,-1):
    
    np1 = [Xlat[0][i], Xlon[0][i]]
    
    if np1[0] > min_lat:
        
        minI = i
        
        min_lat = np1[0]

max_lat = Xlat[row_lat][col_lat]

maxI = col_lat

''' from C to D '''
for i in xrange(col_lat,-1,-1):
    
    np1 = [Xlat[row_lat][i], Xlon[row_long][i]]
    
    if np1[0] < max_lat:
        
        maxI = i
        
        max_lat = np1[0]

min_long = Xlon[0][0]

minJ = 0

''' from A to D '''
for i in xrange(row_lat,-1,-1):
    
    np1 = [Xlat[i][0], Xlon[i][0]]
    
    if np1[1] > min_long:
        
        minJ = i
        
        min_long = np1[1]
    
max_long = Xlon[0][col_long]

maxJ = row_lat

''' from B to C '''
for i in xrange(row_lat,-1,-1):
    
    np1 = [Xlat[i][col_lat], Xlon[i][col_lat]]
    
    if np1[1] < max_long:
        
        maxJ = i
        
        max_long = np1[1]


minLat=np.asscalar(min_lat)
maxLat=np.asscalar(max_lat)
minLon=np.asscalar(min_long)
maxLon=np.asscalar(max_long)

print("minLat: "+str(minLat))
print("maxLat: "+str(maxLat))
print("minLon: "+str(minLon))
print("maxLon: "+str(maxLon))

minimo = ll_to_xy(ncfile, minLat, minLon, timeidx=0, squeeze=True, meta=True, stagger=None, as_int=True)

massimo = ll_to_xy(ncfile, maxLat, maxLon, timeidx=0, squeeze=True, meta=True, stagger=None, as_int=True)

# Interpolazione Per la visualizzazione in stile windy devi avere u10, v10, t2c, rh2, pslp .

minimo = ll_to_xy(ncfile, minLat, minLon, timeidx=0, squeeze=True, meta=True, stagger=None, as_int=True)

massimo = ll_to_xy(ncfile, maxLat, maxLon, timeidx=0, squeeze=True, meta=True, stagger=None, as_int=True)


uvmet10=getvar(ncfile, "uvmet10",meta=True)
#U10Subset = uvmet10[0, to_np(minimo[0]):to_np(massimo[0]) , to_np(minimo[1]):to_np(massimo[1]) ]
#V10Subset = uvmet10[1, to_np(minimo[0]):to_np(massimo[0]) , to_np(minimo[1]):to_np(massimo[1]) ]

#print(np.array(U10Subset))

py = np.array(Xlat)

px = np.array(Xlon)

px = px.flatten()

py = py.flatten()

z = np.array(uvmet10[0])

z = z.flatten()

xi = np.linspace(minLon, maxLon, len(uvmet10[0][0]))

dLon = [j-i for i, j in zip(xi[:-1], xi[1:])]

temp = 0

somma = 0

count = len(xi)

for i, j in zip(xi[:-1], xi[1:]):
    
    temp = j - i 
    
    somma = somma + temp
    
dLon = somma / count

print(dLon)

print("dLon: "+str(dLon))

yi = np.linspace(minLat, maxLat, len(uvmet10[0]))

temp = 0

somma = 0

count = len(yi)

for i, j in zip(yi[:-1], yi[1:]):
    
    temp = j - i 
    
    somma = somma + temp
    
dLat = somma / count

print("dLat: "+str(dLat))

X, Y = np.meshgrid(xi, yi)

U10i = griddata((px,py),z, (X, Y),method='cubic')

#print(U10i)

xi = np.linspace(minLon, maxLon, len(uvmet10[1][0]))

yi = np.linspace(minLat, maxLat, len(uvmet10[1]))

X, Y = np.meshgrid(xi, yi)

z = np.array(uvmet10[1])

z = z.flatten()

V10i = griddata((px,py),z, (X, Y),method='cubic')

fig, ax = plt.subplots()

#Parametri per il file in formato Surfer ASCII

Zmin = cbar_min = np.min(np.array(uvmet10[0]))

Zmax = cbar_max = np.max(np.array(uvmet10[0]))

Xmin = minLon

Xmax = maxLon

Ymin = minLat

Ymax = maxLat

nrows = len(U10i)

ncols = len(U10i[0])

nrowsV = len(V10i)

ncolsV = len(V10i[0])

#creazione del file ascii grid

pathAsciGrid = ''

pathAsciGrid = os.path.join(pathAsciGrid,"asciGrid","asci_grid.grid")

f = open(pathAsciGrid,"w+")

f.write("DSAA\n")

f.write(str(ncols)+" "+str(nrows)+"\n")

f.write(str(Xmin)+" "+str(Xmax)+"\n")

f.write(str(Ymin)+" "+str(Ymax)+"\n")

f.write(str(Zmin)+" "+str(Zmax)+"\n")

for i in range(0, nrows):
    
    for j in range(0, ncols):
        
        f.write(" "+str(U10i[i][j]))

f.close()
    
'''colors = ["#ffffff", "#00ffff", "#0000ff", "#228b22", "#ffff00", "#ffa500", "#ff0000", 	"#ee82ee"]


cmap= matplotlib.colors.ListedColormap(colors,name='from_list', N=None)
cmap.set_under("crimson")
cmap.set_over("w")
norm = matplotlib.colors.Normalize(vmin=cbar_min,vmax=cbar_max)'''

# Interpolate using three different methods and plot
im = plt.contourf(X, Y, U10i)

fig.colorbar(im)

# Componente v della velocita

plt.title('V component')

#plt.show()

#plt.savefig('interpolated.png',dpi=100)
#plt.close(fig)



result = [
    
    {
    
        "header": {
            
            "parameterUnit": "m.s-1", 
             
             "parameterNumber": 2, 
             
             "dx": dLon, 
             
             "dy": dLat, 
             
             "parameterNumberName": "U-component_of_wind", 
             
             "la1": maxLat, 
             
             "la2": minLat, 
             
             "parameterCategory": 2, 
             
             "lo2": maxLon, 
             
             "nx": ncols, 
             
             "ny": nrows, 
             
             "refTime": data_ora, 
             
             "lo1": minLon    
            
            },
     
            "data": []
    
        
    },{
        
        "header": {
     
            "parameterUnit": "m.s-1", 
             
             "parameterNumber": 3, 
             
             "dx": dLon, 
             
             "dy": dLat, 
             
             "parameterNumberName": "U-component_of_wind", 
             
             "la1": maxLat, 
             
             "la2": minLat, 
             
             "parameterCategory": 2, 
             
             "lo2": maxLon, 
             
             "nx": ncols, 
             
             "ny": nrows, 
             
             "refTime": data_ora, 
             
             "lo1": minLon    
        
    }, "data": []
    
    }
]

'''
print("Min lat: "+str(minLat))
print("Min lon: "+str(minLon))
print("Max lat: "+str(maxLat))
print("Max lon: "+str(maxLon))

'''

N = len(U10i) - 1 
 
for i in xrange(N,-1,-1):
    
    for j in range(len(U10i[i])):
        
        result[0]["data"].append(U10i[i][j])

M = len(V10i) - 1

for i in xrange(M,-1,-1):
    
    for j in range(len(V10i[i])):

        result[1]["data"].append(V10i[i][j])

'''
for i in range(0, len(U10i)):
    
    for j in range(0, len(U10i[i])):
                   
        result[0]["data"].append(U10i[i][j])
                   
for i in range(0, len(V10i)):
                   
    for j in range(0, len(V10i[i])):
                   
        result[1]["data"].append(V10i[i][j])'''

pathJsonFile = ''

pathJsonFile = os.path.join(pathJsonFile,"jsonWind","windD03.json")

with open(pathJsonFile, 'w') as f:

    json.dump(result, f)

f.close()


# Modificato il 20/09/2018c alle ore 17:41
