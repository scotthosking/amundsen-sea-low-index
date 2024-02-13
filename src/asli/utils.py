import contextlib
import joblib
from tqdm import tqdm

# https://stackoverflow.com/questions/24983493/tracking-progress-of-joblib-parallel-execution
@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""
    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()


# def write_csv_with_header(df, header, version_id, indata, time_averaging):

#     if (len(all_lows_dfs.time.unique()) < 200):
#         if '-TESTING' not in version_id:
#             version_id = version_id+'-TESTING'

#     if header == 'asli':     
#         fname = indata+'/asli_'+time_averaging+'_v'+version_id+'.csv'
#     if header == 'all_lows': 
#         fname = indata+'/all_lows_'+time_averaging+'_v'+version_id+'.csv'

#     with open('csv_header_asli_v3.txt') as header_file:  
#         lines = header_file.readlines()

#     with open(fname, 'w') as file:
#         for line in lines:
#             if (header == 'all_lows'):
#                 line = line.replace('Amundsen Sea Low (ASL) Index version 3',
#                                     'Detected lows within the Pacific sector of the Southern Ocean')
#             line = line.replace( '<SOURCE_DATA>', indata.upper() )
#             line = line.replace('ASLi_version_id = 3.XXXX', 'ASLi_version_id = '+version_id)
#             line = line.replace('END-OF-FILE','\n')
#             file.write('# '+str(line))

#         df.to_csv(file, index=False)