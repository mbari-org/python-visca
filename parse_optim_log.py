import sys
import numpy as np

cvs_columns = [
    'Timestamp',
    
]

# Example log event:

# ################
# 2024-02-14 08:41:15.154546
# 9050000000000f00030a0a0a000400ff
# 90500c0c0b0430370b0010050d2507ff
# 905001000000000700000000161e15ff
# 90500000000500053838002501031dff 

log_file = sys.argv[1]

with open(log_file,"r") as log:
    
    lines = log.readlines()

log_index = 0

while True:
    
    if log_index >= len(lines):
        break
    
    line = lines[log_index]
    if len(line) >= 16 and '################' in line:
        # log event marker, try to read five more lines
        log_entry = []
        try:
            for i in range(1,6):
                log_entry.append(lines[log_index+i])
            log_index += 6
            # Parse log info and append to csv
            zoom_pos = int(log_entry[1][5:12:2],16)
            focus_pos = int(log_entry[1][17:24:2],16)
            red_gain = int(log_entry[2][5:8:2],16)
            blue_gain = int(log_entry[2][9:12:2],16)
            wb_mode = log_entry[2][13]
            aperture_gain = log_entry[2][15]
            exposure_mode = log_entry[2][17]
            shutter_pos = log_entry[2][20:22]
            iris_pos = log_entry[2][22:24]
            gain_pos = log_entry[2][24:26]
            
            # Create the log row
            log_row = [log_entry[0], 
                       zoom_pos,
                       focus_pos,
                       red_gain,
                       blue_gain,
                       wb_mode,
                       aperture_gain,
                       exposure_mode,
                       shutter_pos,
                       iris_pos,
                       gain_pos
            ]
            print(log_row)
            
        except Exception as e:
            break
    

