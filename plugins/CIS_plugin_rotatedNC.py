from cis.data_io.products.AProduct import AProduct
from cis.data_io.Coord import Coord, CoordList
from cis.data_io.ungridded_data import UngriddedData, UngriddedCoordinates
from cis.data_io.ungridded_data import Metadata
import numpy as np
import iris

class MyPluginBaby(AProduct):

    def get_file_signature(self):
        return [r'.*.rnc']

    def _create_coord_list(self, filenames, data=None):
        if data is None:
                data = {}
                NPoleLon=147
                NPoleLat=68
                ma = iris.load_cube(filenames)
                rlon = ma.coord('grid_longitude').points
                rlat = ma.coord('grid_latitude').points
                tim  = ma.coord('time').points
                data["time"] = np.repeat(tim,len(rlon)*len(rlat))
                rlonGrd,rlatGrd = np.meshgrid(rlon,rlat)
                lonsGrd,latsGrd = iris.analysis.cartography.unrotate_pole(rlonGrd,rlatGrd,NPoleLon,NPoleLat)
                data["longitude"]=np.tile(lonsGrd.flatten(),len(tim))
                data["latitude"]=np.tile(latsGrd.flatten(),len(tim))
        coords = CoordList()
        coords.append(Coord(data['longitude'],Metadata(name="longitude",long_name='longitude',standard_name='longitude',shape=(len(data),),missing_value=-999.0,units="degrees_east",range=(-180, 180)),"x"))
        coords.append(Coord(data['latitude'],Metadata(name="latitude",long_name='latitude',standard_name='latitude',shape=(len(data),),missing_value=-999.0,units="degrees_north",range=(-90, 90)),"y"))
        coords.append(Coord(data['time'],Metadata(name="time",long_name='time',standard_name='time',shape=(len(data),),missing_value=-999.0,units="days since 1600-01-01 00:00:00"),"t"))
        return coords

    def create_coords(self, filenames, variable=None):
        return UngriddedCoordinates(self._create_coord_list(filenames))

    def create_data_object(self, filenames, variable):
        data_dict = {}
        NPoleLon=147
        NPoleLat=68
        ma = iris.load_cube(filenames)
        rlon = ma.coord('grid_longitude').points
        rlat = ma.coord('grid_latitude').points
        tim  = ma.coord('time').points
        data_dict["time"] = np.repeat(tim,len(rlon)*len(rlat))
        aod = ma.data
        rlonGrd,rlatGrd = np.meshgrid(rlon,rlat)
        lonsGrd,latsGrd = iris.analysis.cartography.unrotate_pole(rlonGrd,rlatGrd,NPoleLon,NPoleLat)
        data_dict["longitude"]=np.tile(lonsGrd.flatten(),len(tim))
        data_dict["latitude"]=np.tile(latsGrd.flatten(),len(tim))
        data_dict["aod"]=aod.flatten()
        coords = self._create_coord_list(filenames,data_dict)
        return UngriddedData(data_dict["aod"],Metadata(name="aod",long_name='atmosphere_optical_thickness_due_to_dust_ambient_aerosol',standard_name='atmosphere_optical_thickness_due_to_dust_ambient_aerosol',shape=(len(data_dict),),missing_value=-999.0,units="1"),coords)
        
    def get_variable_names(self, filenames, data_type=None):
        return ['Info unavailable with this plugin']