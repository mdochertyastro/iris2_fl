import numpy as np
import copy


def tag_extract(iris2model,tagname): #tagname is a string from tag_print() list
    '''inital extraction of tags from iris2model numpy.record'''
    tag=iris2model[tagname]
    tag=copy.deepcopy(tag) # make them writable
    tag.setflags(write=1)
    return tag

def kpeak_ind_extract(wavelength): # wavelength from iris2model - this is to eventually get the max contrast iris_cal frame to get the FL mask
    '''Extract wavelength index corresponding to kpeak'''
    kpeak=2795.528 #from iris docs - itn39
    kpeak_ind=np.argmin(abs(wavelength-kpeak))
   
    return kpeak_ind

def trimmed_rows(frame): # returns 2 entry list for max/min rows of non-zero observation (this is important for cdelt aspect and extent later)
    '''Using centre column intensities, return a len(2) list giving min/max row values of observation'''
    centre_pixel=[]
    for dim in frame.shape:
        centre_pixel.append(round(dim/2))
    row_min=[]
    row_max=[]
    for ind, row in enumerate(frame[:,centre_pixel[1]]):
          if row==0:
                if ind<centre_pixel[0]:
                    row_min.append(ind)   
                else:
                    row_max.append(ind)       
    trimmed_rows=[1+np.max(row_min),-1+np.min(row_max)]
    
    return trimmed_rows


def data_trim(tag,trimmed_rows,tagname=None):
    '''Using trimmed rows, reshapes data to exclude IRIS observation borders and the first/last ltau values as their unc is ridiculously large'''
    row_min=trimmed_rows[0]
    row_max=trimmed_rows[1]
    
    if tagname=='ltau':
        tag=tag[1:-1]
    if tagname=='iris_cal':
        tag=tag[:,row_min:row_max,:]
    if tagname=='model' or tagname=='uncertainty':
        tag=tag[:,1:-1,row_min:row_max,:]
        
    print(f'{tagname} has successfully been trimmed to {tag.shape}')
    return tag
    
def frames_extract(model):
    '''Creates a list of model frames for each ltau value (post-trim so no need for nans)'''
    frames_list=[]
    for index in range(model.shape[0]):
        frame=model[index,...]
        frames_list.append(frame)
    return frames_list