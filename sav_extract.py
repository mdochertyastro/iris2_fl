import fnmatch
from scipy.io import readsav
import numpy 
import glob

def sav_extract(filename,nras=None):

    '''
    Reads in IDL .sav files after a series of tests to ensure correct file is read in. 
    Note: Multiple rasters inverted into one file need to have 'multi' in their name
    Note: For multi files, to extract one raster into a numpy.record need to give kwarg: nras=5 for example
    ''' 
    
    ### Ensures filename exists/is in cwd
    if not glob.glob(filename):
        print(f'file {filename} does not exist or is not in cwd')
        return
    
    ### Assuming it is, we have more tests:
    else:
        if fnmatch.fnmatch(filename, '*.sav')==False: #check that it's a .sav file
            print(f'{filename} is not a .sav file')
            return

        output_record=[]
        
        ### If filename contains 'multi' it is an inversion of multiple rasters so has to be dealt with differently
        if fnmatch.fnmatch(filename, '*multi*'):
            output_array=readsav(filename)['iris2model']
            
            ### If no raster number is specified then return all inversions as a numpy.recarray
            if nras is None:
                print(f'Your file {filename} contains an inversion of {len(output_array)} rasters, no raster number was selected so will return numpy.recarray of all {len(output_array)} rasters...')
                
                ### Double check the structre of the numpy output is as expected - in this case a recarray
                if type(output_array)==numpy.recarray:
                    print('...with the required structure')
                    return output_array
                else:
                    print('... woops, wrong structure')
                    return

            ### If raster number is specified, return that raster's inversion as a numpy.record        
            else:
                output_record=output_array[nras]
                print(f'Your file {filename} contains an inversion of {len(output_array)} rasters and raster {nras} will be returned as a numpy.record...')
                
                ### Double check the strcutre of the numpy output is as expected - in this case a record
                if type(output_record)==numpy.record:
                    print('...with the required structure')
                    return output_record
                else:
                    print('... woops, wrong structure')
                    return   
        
        ### If filename doesn't contain 'multi' then it is a single raster inversion
        else:
            output_array=readsav(filename)['iris2model']
            output_record=output_array[0]
            print(f'Your file {filename} contains an inversion of a single raster and will be returned as a numpy.record...')
            
            ### Double check the structre of the numpy output is as expected - in this case a recarray
            if type(output_record)==numpy.record:
                print('...with the required structure')
                return output_record
            else:
                print('... woops, wrong structure')
                return
        
    
    
    
    
    