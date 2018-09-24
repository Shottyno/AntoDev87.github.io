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

dLon = 0.25

dLat = 0.25

url = "http://193.205.230.6:8080/opendap/hyrax/opendap/wrf5/d01/20180909Z00/wrfout_d01_2018-09-09_02%3A00%3A00.nc"

splitted = url.split("/")

arr_data_ora = splitted[9].replace("%3A", ":").split("_")

data_ora = arr_data_ora[2]+" "+arr_data_ora[3].replace(".nc", "")

#ncfile = Dataset("http://193.205.230.6:8080/opendap/opendap/wrf5/d03/20180702Z00/wrfout_d03_2018-07-06_00%3A00%3A00.nc")
ncfile = Dataset("http://193.205.230.6:8080/opendap/hyrax/opendap/wrf5/d01/20180909Z00/wrfout_d01_2018-09-09_02%3A00%3A00.nc")
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

yi = np.linspace(minLat, maxLat, len(uvmet10[0]))

X, Y = np.meshgrid(xi, yi)

U10i = griddata((px,py),z, (X, Y),method='cubic')

#print(U10i)

xi = np.linspace(minLon, maxLon, len(uvmet10[1]))

yi = np.linspace(minLat, maxLat, len(uvmet10[1][0]))

X, Y = np.meshgrid(xi, yi)

z = np.array(uvmet10[1])

z = z.flatten()

V10i = griddata((px,py),z, (X, Y),method='cubic')

print(U10i)


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

f = open("asci_grid.grid","w+")

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

'''result=[ {
  "header": {
    "discipline":0,
    "disciplineName":"Meteorological products",
    "gribEdition":2,
    "gribLength":76420,
    "center":7,
    "centerName":"US National Weather Service - NCEP(WMC)",
    "subcenter":0,
    "refTime":data_ora,
    "significanceOfRT":1,
    "significanceOfRTName":"Start of forecast",
    "productStatus":0,
    "productStatusName":"Operational products",
    "productType":1,
    "productTypeName":"Forecast products",
    "productDefinitionTemplate":0,
    "productDefinitionTemplateName":"Analysis/forecast at horizontal level/layer at a point in time",
    "parameterCategory":2,"parameterCategoryName":"Momentum",
    "parameterNumber":2,
    "parameterNumberName":"U-component_of_wind",
    "parameterUnit":"m.s-1",
    "genProcessType":2,
    "genProcessTypeName":"Forecast",
    "forecastTime":0,
    "surface1Type":103,
    "surface1TypeName":"Specified height level above ground",
    "surface1Value":10.0,
    "surface2Type":255,
    "surface2TypeName":"Missing",
    "surface2Value":0.0,
    "gridDefinitionTemplate":0,
    "gridDefinitionTemplateName":"Latitude_Longitude",
    "numberPoints":65160,
    "shape":6,
    "shapeName":"Earth spherical with radius of 6,371,229.0 m",
    "gridUnits":"degrees",
    "resolution":48,
    "winds":"true",
    "scanMode":0,
    "nx":nrows,
    "ny":ncols,
    "basicAngle":0,
    "subDivisions":0,
    "lo1":minLon,
    "la1":maxLat,
    "lo2":maxLon,
    "la2":minLat,
    "dx":dLon,
    "dy":dLat },
  "data": [
            
            
  ]},{
  "header": {
    "discipline":0,
    "disciplineName":"Meteorological products",
    "gribEdition":2,
    "gribLength":76420,
    "center":7,
    "centerName":"US National Weather Service - NCEP(WMC)",
    "subcenter":0,
    "refTime":data_ora,
    "significanceOfRT":1,
    "significanceOfRTName":"Start of forecast",
    "productStatus":0,
    "productStatusName":"Operational products",
    "productType":1,
    "productTypeName":"Forecast products",
    "productDefinitionTemplate":0,
    "productDefinitionTemplateName":"Analysis/forecast at horizontal level/layer at a point in time",
    "parameterCategory":2,"parameterCategoryName":"Momentum",
    "parameterNumber":2,
    "parameterNumberName":"U-component_of_wind",
    "parameterUnit":"m.s-1",
    "genProcessType":2,
    "genProcessTypeName":"Forecast",
    "forecastTime":0,
    "surface1Type":103,
    "surface1TypeName":"Specified height level above ground",
    "surface1Value":10.0,
    "surface2Type":255,
    "surface2TypeName":"Missing",
    "surface2Value":0.0,
    "gridDefinitionTemplate":0,
    "gridDefinitionTemplateName":"Latitude_Longitude",
    "numberPoints":65160,
    "shape":6,
    "shapeName":"Earth spherical with radius of 6,371,229.0 m",
    "gridUnits":"degrees",
    "resolution":48,
    "winds":"true",
    "scanMode":0,
    "nx":nrowsV,
    "ny":ncolsV,
    "basicAngle":0,
    "subDivisions":0,
    "lo1":minLon,
    "la1":maxLat,
    "lo2":maxLon,
    "la2":minLat,
    "dx":dLon,
    "dy":dLat },
  "data": [
            
            
  ]}
]'''


result = [
    
    {
    
        "header": {
     
        "discipline":0,
        "disciplineName":"Meteorological products",
        "gribEdition":2,
        "gribLength":76420,
        "center":7,
        "centerName":"US National Weather Service - NCEP(WMC)",
        "subcenter":0,
        "refTime":data_ora,
        "significanceOfRT":1,
        "significanceOfRTName":"Start of forecast",
        "productStatus":0,
        "productStatusName":"Operational products",
        "productType":1,
        "productTypeName":"Forecast products",
        "productDefinitionTemplate":0,
        "productDefinitionTemplateName":"Analysis/forecast at horizontal level/layer at a point in time",
        "parameterCategory":2,"parameterCategoryName":"Momentum",
        "parameterNumber":2,
        "parameterNumberName":"U-component_of_wind",
        "parameterUnit":"m.s-1",
        "genProcessType":2,
        "genProcessTypeName":"Forecast",
        "forecastTime":0,
        "surface1Type":103,
        "surface1TypeName":"Specified height level above ground",
        "surface1Value":10.0,
        "surface2Type":255,
        "surface2TypeName":"Missing",
        "surface2Value":0.0,
        "gridDefinitionTemplate":0,
        "gridDefinitionTemplateName":"Latitude_Longitude",
        "numberPoints":ncols*nrows,
        "shape":6,
        "shapeName":"Earth spherical with radius of 6,371,229.0 m",
        "gridUnits":"degrees",
        "resolution":48,
        "winds":"true",
        "scanMode":0,
            
        "nx": ncols,
        
        "ny": nrows,
    
        "basicAngle":0,
    
        "subDivisions":0,
            
        "la1":Xmax,
            
        "la2":Xmin,
            
        "lo1":Ymin, 
        
        "lo2":Ymax,
            
        "dx": dLon,
        
        "dy": dLat,
            
    }, "data": []
    
        
    },{
        
        "header": {
     
            "discipline":0,
            "disciplineName":"Meteorological products",
            "gribEdition":2,
            "gribLength":76420,
            "center":7,
            "centerName":"US National Weather Service - NCEP(WMC)",
            "subcenter":0,
            "refTime":data_ora,
            "significanceOfRT":1,
            "significanceOfRTName":"Start of forecast",
            "productStatus":0,
            "productStatusName":"Operational products",
            "productType":1,
            "productTypeName":"Forecast products",
            "productDefinitionTemplate":0,
            "productDefinitionTemplateName":"Analysis/forecast at horizontal level/layer at a point in time",
            "parameterCategory":2,"parameterCategoryName":"Momentum",
            "parameterNumber":3,
            "parameterNumberName":"U-component_of_wind",
            "parameterUnit":"m.s-1",
            "genProcessType":2,
            "genProcessTypeName":"Forecast",
            "forecastTime":0,
            "surface1Type":103,
            "surface1TypeName":"Specified height level above ground",
            "surface1Value":10.0,
            "surface2Type":255,
            "surface2TypeName":"Missing",
            "surface2Value":0.0,
            "gridDefinitionTemplate":0,
            "gridDefinitionTemplateName":"Latitude_Longitude",
            "numberPoints":ncols*nrows,
            "shape":6,
            "shapeName":"Earth spherical with radius of 6,371,229.0 m",
            "gridUnits":"degrees",
            "resolution":48,
            "winds":"true",
            "scanMode":0,
            "nx": ncols,
        
            "ny": nrows,
            "basicAngle":0,
            "subDivisions":0,
          
            "la1":Xmax,
            
            "la2":Xmin,
            
            "lo1":Ymin, 
        
            "lo2":Ymax,
            
            "dx":dLon,
            "dy":dLat    
        
        
    
    }, "data": []
    
    }
]


print("Min lat: "+str(minLat))
print("Min lon: "+str(minLon))
print("Max lat: "+str(maxLat))
print("Max lon: "+str(maxLon))

for i in range(0, nrows):
    
    for j in range(0, ncols):

        result[0]["data"].append(U10i[i][j])

for i in range(0, nrowsV):
    
    for j in range(0, ncolsV):

        result[1]["data"].append(V10i[i][j])


with open('wind.json', 'w') as f:

    json.dump(result, f)

f.close()
