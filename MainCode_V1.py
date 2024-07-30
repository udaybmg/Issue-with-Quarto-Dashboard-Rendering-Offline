import subprocess
import os
import zipfile
import csv
import shutil
import pandas as pd
from datetime import datetime
import yaml
from pytz import timezone
import datetime as dt

_path = r'C:\Users\perrottalison\OneDrive - Meta\Documents\Data\Lot_Summary_Data\C4270'
Task = 'T196524403'

# Hardcoded variables:
Simulation = True # set to False if running on new data
output_meta_data_csv = r'C:\Users\perrottalison\OneDrive - Meta\Documents\Data\Lot_Summary_Data\C4264\Supplementary_Material\C4264.1_Meta_Data.csv' # csv file used for simulations
short_device_current_limit = 1e-11 # defines the short device in DAT401 & DAT410 measurement
short_device_voltage_limit = 0.5 # defines the short device in DAT420 & DAT421 measurement

short_device_voltage_limit_DAT431 = 0.5 # defined in the Test Butler DAT431 script
"""
DO NOT EDIT BELOW THIS LINE UNLESS YOU ARE 100% SURE.
"""

short_device_current_limit_pA = short_device_current_limit * 1e12
task_number = Task.split('T')[-1]
os.environ["TASK_NUMBER"] = task_number
os.environ["short_device_current_limit_pA"] = str(short_device_current_limit_pA)
os.environ["short_device_voltage_limit"] = str(short_device_voltage_limit)
os.environ["short_device_voltage_limit_DAT431"] = str(short_device_voltage_limit_DAT431)

# Output csv file
if not os.path.exists(f'{_path}/Supplementary_Material'):
    os.mkdir(f'{_path}/Supplementary_Material')

# Read data from csv file using multi-indexing to make it easier to reference later
df_meta_data = pd.read_csv(output_meta_data_csv, index_col=['device_id', 'zone', 'subcell']).sort_index()
Lot_id = df_meta_data['lot_id'].unique()[0]
_path = r'C:\Users\perrottalison\OneDrive - Meta\Documents\Data\Lot_Summary_Data\C4264'

os.environ["CSV_PATH"] = output_meta_data_csv
timestamp = dt.datetime.now(dt.timezone.utc)
timestamp = timestamp.astimezone(timezone('Europe/Dublin'))
timestamp = timestamp.strftime('%Y%m%d-%H%M%SZ')

# Write variables and file path _quarto.yml file
# Define your data structure
data = {
    "title": "Summary for " + Lot_id,
    "output-file": Lot_id + "_Summary_" + timestamp + ".html",
    "project": {
        "output-dir": _path + "/"
    },
    "date": "today",
    "date-format": "long",
    "format": {
        "dashboard": {
            "scrolling": True,
            "link-external-newwindow": True,
            "embed-resources": True
        }
    },
    "execute": {
        "echo": False,
        "enabled": True
    },
    "theme": "custom.scss",
    "jupyter": "python3"
}

# Open the file in write mode ("w")
with open("_quarto.yml", "w") as f:
    # Dump the data to the file using the YAML dumper
    yaml.dump(data, f)

# Block to render Quarto to html
terminalcom_1 = 'quarto render Dashboard_V1.ipynb'

subprocess.run(terminalcom_1.split(), shell=True, check=True)
