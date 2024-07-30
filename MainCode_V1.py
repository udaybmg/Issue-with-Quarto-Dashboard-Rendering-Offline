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
import pathlib

Task = 'T12345'

_path = pathlib.Path(__file__).parent
output_meta_data_csv = _path / 'A1234_Data.csv'

# Hardcoded variables:
#output_meta_data_csv = _path+'\A1234_Data.csv' # csv file used for simulations
short_device_current_limit = 1e-11
short_device_voltage_limit = 0.5


short_device_current_limit_pA = short_device_current_limit * 1e12
task_number = Task.split('T')[-1]
os.environ["TASK_NUMBER"] = task_number
os.environ["short_device_current_limit_pA"] = str(short_device_current_limit_pA)
os.environ["short_device_voltage_limit"] = str(short_device_voltage_limit)

# Read data from csv file using multi-indexing to make it easier to reference later
df_meta_data = pd.read_csv(output_meta_data_csv, index_col=['device_id', 'zone', 'subcell']).sort_index()
Lot_id = df_meta_data['lot_id'].unique()[0]

# os.environ["CSV_PATH"] = output_meta_data_csv
os.environ["CSV_PATH"] = str(output_meta_data_csv)
timestamp = dt.datetime.now(dt.timezone.utc)
timestamp = timestamp.astimezone(timezone('Europe/Dublin'))
timestamp = timestamp.strftime('%Y%m%d-%H%M%SZ')

path_dir=str(_path)
# Write variables and file path _quarto.yml file
# Define your data structure
data = {
    "title": "Summary for " + Lot_id,
    "output-file": Lot_id + "_Summary_" + timestamp + ".html",
    "project": {
        "output-dir": path_dir + "/"
    },
    "date": "today",
    "date-format": "long",
    "format": {
        "dashboard": {
            "scrolling": True,
            "link-external-newwindow": True,
            "embed-resources": False
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
