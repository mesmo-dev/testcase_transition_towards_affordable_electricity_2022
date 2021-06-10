"""Example script for grabbing OpenDSS commands from FLEDGE to created a DSS file."""

import cvxpy as cp
import logging
import numpy as np
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import fledge

def main():

    # Settings.
    scenario_name = 'singapore_geylang'
    results_path = fledge.utils.get_results_path(__file__, scenario_name)

    # Recreate / overwrite database, to incorporate changes in the CSV files.
    fledge.config.config['paths']['additional_data'].append(
        os.path.join(os.path.dirname(os.path.dirname(os.path.normpath(__file__))), 'data', 'fledge')
    )
    fledge.data_interface.recreate_database()

    # Stream OpenDSS commands to log file.
    fledge.electric_grid_models.logger.setLevel(logging.DEBUG)
    fledge.electric_grid_models.logger.addHandler(logging.FileHandler(os.path.join(results_path, f'{scenario_name}.log')))

    # Create OpenDSS model.
    fledge.electric_grid_models.ElectricGridModelOpenDSS(scenario_name)

    # Create DSS file from logged DSS commands.
    with open(os.path.join(results_path, f'{scenario_name}.log'), 'r') as oldfile, \
            open(os.path.join(results_path, f'{scenario_name}.dss'), 'w') as newfile:
        for line in oldfile:
            if 'opendss_command_string =' not in line:
                newfile.write(line)

    # Print results path.
    fledge.utils.launch(results_path)
    print(f"Results are stored in: {results_path}")


if __name__ == '__main__':
    main()
