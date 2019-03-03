# EELSData.py

import numpy as np
import pathlib as pl
import pandas as pd
from PIL import Image

keys = ['AG', 'FC_wide', 'FC_close', 'FCVC_wide', 'FCVC_close']

TEM_root = pl.Path("../Figures/TEM/Junwei's Images")

data_paths = {'AG': TEM_root / pl.Path('As Grown/Plain/'),
              'FC_wide': TEM_root / pl.Path('Field Cooled/EELS_wide'),
              'FC_close': TEM_root / pl.Path('Field Cooled/EELS_close'),
              'FCVC_wide': TEM_root / pl.Path('Field Cooled Voltage Conditioned/EELS_wide'),
              'FCVC_close': TEM_root / pl.Path('Field Cooled Voltage Conditioned/EELS_close')
              }

data_element_files = {key: [name for name in value.iterdir() if 'EELS_' in name.name]
                      for key, value in data_paths.items()}
images = {key: np.array(Image.open(value / 'EELS.png').convert('L')) for key, value in data_paths.items()}
labels = {'AG': 'As grown',
          'FC_wide': 'Field cooled',
          'FC_close': 'Field cooled',
          'FCVC_wide': 'Field Cooled+Voltage Conditioned',
          'FCVC_close': 'Field Cooled+Voltage Conditioned'}

image_sizes_x = {'AG': 334, 'FC_wide': 329, 'FC_close': 6.53, 'FCVC_wide': 276, 'FCVC_close': 20.4}
element_linestyles = {'Si': '-', 'Co': '-', 'Ni': '-', 'Pt': '-', 'Gd': '-', 'O': '-', 'Al': '-'}
element_colors = {'Si': 'black',
                  'Co': 'midnightblue',
                  'Ni': 'darkgreen',
                  'Pt': 'grey',
                  'Gd': 'darkgoldenrod',
                  'O': 'sienna',
                  'Al': 'red'}

limits_x = {'AG': (65, 85), 
            'FC_wide': (0, image_sizes_x['FC_wide']), 
            'FC_close': (0, image_sizes_x['FC_close']), 
            'FCVC_wide': (0, image_sizes_x['FCVC_wide']), 
            'FCVC_close': (0, image_sizes_x['FCVC_close'])}


def integrate_y(arr, normalize=True):
    integral = np.sum(arr, axis=0)

    if normalize:
        sorted_integral = np.sort(integral)
        median_of_top_bins = np.median(sorted_integral[-50:])
        median_of_bottom_bins = np.median(sorted_integral[:50])
        return (integral - median_of_bottom_bins)/(median_of_top_bins-median_of_bottom_bins)    # Normalize the integral
    else:
        return integral


def get_element(path):
    return path.stem.split('_')[-1].capitalize()


def load_image(path):
    return np.array(Image.open(path).convert('L'))


def generate_data_structure():
    data = dict()
    for key in keys:
        data[key] = pd.DataFrame()
        for element_path in data_element_files[key]:
            element = get_element(element_path)
            data[key][element] = integrate_y(load_image(element_path), normalize=True)
        data[key]['x'] = np.linspace(0, image_sizes_x[key], data[key].shape[0])
    return data


def write_pandas_data(data, output_dir):
    for key, df in data.items():
        with open('{}/{}_{}'.format(pl.Path(output_dir).as_posix(), key, 'EELS_table.csv'), 'w') as f:
            df.to_csv(f, index=False)

data = generate_data_structure()
