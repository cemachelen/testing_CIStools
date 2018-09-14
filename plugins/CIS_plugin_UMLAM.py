from cis.data_io.products.AProduct import AProduct
from cis.data_io.Coord import Coord, CoordList
from cis.data_io.ungridded_data import UngriddedData,UngriddedCoordinates
from cis.data_io.ungridded_data import Metadata
import iris
import numpy as np
import cf_units

class UMLAM(AProduct):

    def get_file_signature(self):
        return [r'.*.UMLAM']

    def _create_coord_list(self, filenames, data=None):
        if data is None:
            #Load cubes:
            ma = iris.load(filenames)
            ma = ma.concatenate_cube()
            #Extract lat, lon and time:
            lon2D = ma.coord('longitude').points
            lat2D = ma.coord('latitude').points
            origTimes  = ma.coord('time').points
            #Convert time to days since 
            niceDateTime = cf_units.num2date(origTimes,'hours since 2011-05-01 00:00:00', 'gregorian')
            reqdDateTime = cf_units.date2num(niceDateTime,'days since 1600-01-01 00:00:00', 'gregorian')
            #'Unravel' data:
            data = {}
            data['longitude'] = np.tile(lon2D.flatten(),len(origTimes))
            data['latitude'] = np.tile(lat2D.flatten(),len(origTimes))
            data['time'] = np.repeat(reqdDateTime,lon2D.size)
        coords = CoordList() #initialise coordinate list
        #Append latitudes and longitudes to coordinate list:
        coords.append(Coord(data['longitude'],Metadata(name="longitude",long_name='longitude',standard_name='longitude',shape=(len(data),),missing_value=-999.0,units="degrees_east",range=(-180, 180)),"x"))
        coords.append(Coord(data['latitude'],Metadata(name="latitude",long_name='latitude',standard_name='latitude',shape=(len(data),),missing_value=-999.0,units="degrees_north",range=(-90, 90)),"y"))
        coords.append(Coord(data['time'],Metadata(name="time",long_name='time',standard_name='time',shape=(len(data),),missing_value=-999.0,units="days since 1600-01-01 00:00:00"),"t"))
        return coords

    def create_coords(self, filenames, variable=None):
        return UngriddedCoordinates(self._create_coord_list(filenames))

    def create_data_object(self, filenames, variable):
        #Load cubes:
        ma = iris.load(filenames)
        ma = ma.concatenate_cube()
        #Extract lat, lon, time and variable:
        lon2D = ma.coord('longitude').points
        lat2D = ma.coord('latitude').points
        origTimes  = ma.coord('time').points
        var2D = ma.data
        #Convert time to days since 
        niceDateTime = cf_units.num2date(origTimes,'hours since 2011-05-01 00:00:00', 'gregorian')
        reqdDateTime = cf_units.date2num(niceDateTime,'days since 1600-01-01 00:00:00', 'gregorian')
        #'Unravel' data:
        data_dict = {}
        data_dict['longitude'] = np.tile(lon2D.flatten(),len(origTimes))
        data_dict['latitude'] = np.tile(lat2D.flatten(),len(origTimes))
        data_dict['time'] = np.repeat(reqdDateTime,lon2D.size)
        data_dict[variable]=var2D.flatten()
        coords = self._create_coord_list(filenames,data_dict)
        return UngriddedData(data_dict[variable],Metadata(name=variable,long_name=variable,shape=(len(data_dict),),missing_value=-999.0,units="1"),coords)
        
    def get_variable_names(self, filenames, data_type=None):
        return ['Info unavailable with this plugin']