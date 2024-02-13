


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