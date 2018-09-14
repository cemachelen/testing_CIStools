from cis.data_io.products.AProduct import AProduct
from cis.data_io.Coord import Coord, CoordList
from cis.data_io.ungridded_data import UngriddedData,UngriddedCoordinates
from cis.data_io.ungridded_data import Metadata
import netCDF4
import numpy as np
import iris


class MODIS_rerotated(AProduct):

    def get_file_signature(self):
        return [r'.*.modrr']

    def _create_coord_list(self, filenames, data=None):
        if data is None:
            data = {} #initialise data dictionary
            inData=netCDF4.Dataset(filenames[0]) #open netCDF file
            lons=np.array(inData.variables['longitude']) #extract longitudes
            lats=np.array(inData.variables['latitude']) #extract latitudes
            lons_rotated,lats_rotated = iris.analysis.cartography.unrotate_pole(lons,lats,180.86,70.53)
            data['longitude']=lons_rotated
            data['latitude']=lats_rotated
            data['time']=np.array(inData.variables['time']) #extract times
            inData.close() #close netCDF file
        coords = CoordList() #initialise coordinate list
        #Append latitudes and longitudes to coordinate list:
        coords.append(Coord(data['longitude'],Metadata(name="longitude",long_name='longitude',standard_name='longitude',shape=(len(data),),missing_value=np.nan,units="degrees_east",range=(-180, 180)),"x"))
        coords.append(Coord(data['latitude'],Metadata(name="latitude",long_name='latitude',standard_name='latitude',shape=(len(data),),missing_value=np.nan,units="degrees_north",range=(-90, 90)),"y"))
        coords.append(Coord(data['time'],Metadata(name="time",long_name='time',standard_name='time',shape=(len(data),),missing_value=np.nan,units="days since 1600-01-01 00:00:00"),"t"))
        return coords

    def create_coords(self, filenames, variable=None):
        return UngriddedCoordinates(self._create_coord_list(filenames))

    def create_data_object(self, filenames, variable):
        data = {} #initialise data dictionary
        inData=netCDF4.Dataset(filenames[0]) #open netCDF file
        lons=np.array(inData.variables['longitude']) #extract longitudes
        lats=np.array(inData.variables['latitude']) #extract latitudes
        lons_rotated,lats_rotated = iris.analysis.cartography.unrotate_pole(lons,lats,180.86,70.53)
        data['longitude']=lons_rotated
        data['latitude']=lats_rotated
        data['time']=np.array(inData.variables['time']) #extract times
        data[variable]=np.array(inData.variables[variable])  #extract requested variable
        inData.close() #close netCDF file
        coords = self._create_coord_list(filenames,data)
        return UngriddedData(data[variable],Metadata(name=variable,long_name=variable,units='1',shape=(len(data),),missing_value=np.nan),coords)

    def get_variable_names(self, filenames, data_type=None):
        return ['Info unavailable with this plugin']
