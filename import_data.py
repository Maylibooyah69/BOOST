# %%
# importing lib
import unittest
import numpy as np
import plotly.express as px
import pandas as pd
import h5py,os,re,datetime
# %%
#define constants and file paths
#
BOOST2_data_path='/Users/genepan/datasets/Boost2/BOOST-II_UTAH_MOBERG_CLEANED_HDF5_FILES'
hdf5_paths=[]
for root,dirs,files in os.walk(BOOST2_data_path):
    for name in dirs:
        for sub_root,_,file_names in os.walk(os.path.join(root, name)):
            for file_name in file_names:
                if 'hdf5' in file_name:
                    hdf5_paths.append(os.path.join(sub_root,file_name))


# %%
#helper functions
def read_hdf5_file(file_path,target_fields=['ICP']):
    '''Generates some metadata from the hdf5 file and obtain 
    specified data field'''
    h5py_object=h5py.File(file_path,'r')
    dict_of_fields={'waves':np.array(h5py_object['waves']),'numerics':np.array(h5py_object['numerics'])}
    #obtain metadata
    meta_data_fields,meta_data_dict,target_dict=['duration','dataStartTime'],{},{}
    [meta_data_dict.update({key:np.array(h5py_object.attrs[key])[0].decode('UTF-8')}) for key in meta_data_fields]
    meta_data_dict['patient_info']=np.array(h5py_object['patient.info'])

    #target_fields and package into a pandas dataframe
    for field in target_fields:
        for sub_dir,sub_field_lst in dict_of_fields.items():
            for sub_field in sub_field_lst:
                for target_field in target_fields:
                    if target_field in sub_field:
                        print('haha',sub_dir,sub_field)
                        if 'index' in target_field:
                            target_dict[sub_dir+'_'+sub_field].attrs['index']=target_field
                        target_dict[sub_dir+'_'+sub_field]=h5py_object[sub_dir][sub_field]
    return target_dict,meta_data_dict #np.array(h5py_object)

    #there's a middle step here I fix the external index issue

def extract_field_data(target_field,standardize_freq=500):
    '''output each standardized time segment into a list,
    pass in one field at a time'''
    pd_series_dict={}
    for field_name,field_data in target_field.items():
        if 'index' in field_name:
            index_vec=np.array(field_data)
        else:
            index_vec=np.array(field_data.attrs['index'])
            # data=pd.Series(field_data,pd.to_timedelta(np.arange(len(np.array(field_data))),unit=str()+'ms'))
    for time_segment in index_vec:
        start_index,start_time,seg_length,freq=time_segment
        duration=seg_length/freq
        # print(seg_length,freq,duration,start_time)
        data=pd.Series(field_data[start_index:start_index+seg_length],
        pd.to_timedelta(np.linspace(0,
        duration,seg_length),'s')+datetime.datetime.fromtimestamp(start_time/1000000.0))
        pd_series_dict[str(start_time)]=data
    return pd.DataFrame(pd_series_dict)


# %%
my_data=extract_field_data(my_target_dict)
my_data
# %%
filtered_df=my_data[pd.notna(my_data).iloc[:,0]]
px.line(filtered_df,x=filtered_df.index,y=filtered_df.columns[0])
# %%

filtered_df.plot()
# %%
# pd.to_timedelta(np.arange(365635),unit='ms')
# upsampled=my_data.resample('S').asfreq()
# upsampled
px.scatter(my_data)
my_data
# %%
my_target_dict,metadata=read_hdf5_file(hdf5_paths[3],['ICP'])

# for path in hdf5_paths:
#     read_hdf5_file(path,['ICP'])

# %%
my_target_dict['numerics_PbtO2.index'].name
# %%
#gen
np.array(my_target_dict['waves_ICP'].attrs['index']).shape

# data_frame_index=str(np.array(my_target_dict['waves_ICP'].attrs['index']).dtype).split(')')
# pd.DataFrame(np.array(my_target_dict['waves_ICP'].attrs['index']),np.array(my_target_dict['waves_ICP'].attrs['index']).dtype[0])

# %%
str(np.array(my_target_dict['waves_ICP'].attrs['index']).dtype).split(')')
#extract all ICP 
# %%
data_frame_index


# Seems like folder 5008 and 5007 are corrupted
