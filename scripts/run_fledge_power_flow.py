"""Example script for setting up and solving an single step electric grid power flow problem."""

import cvxpy as cp
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

    # Obtain scenario data.
    # - This contains general information, e.g. the base power values which are needed for the plots below.
    scenario_data = fledge.data_interface.ScenarioData(scenario_name)

    # Obtain electric grid model.
    # - The ElectricGridModelDefault object defines index sets for node names / branch names / der names / phases /
    #   node types / branch types, the nodal admittance / transformation matrices, branch admittance /
    #   incidence matrices, DER incidence matrices and no load voltage vector as well as nominal power vector.
    # - The model is created for the electric grid which is defined for the given scenario in the data directory.
    electric_grid_model = fledge.electric_grid_models.ElectricGridModelDefault(scenario_name)

    # Obtain the nominal DER power vector.
    der_power_vector_nominal = electric_grid_model.der_power_vector_reference

    # Obtain power flow solution.
    # - The power flow solution object obtains the solution for nodal voltage vector / branch power vector
    #   and total loss (all complex valued) for the given DER power vector.
    # - There are different power flow solution objects depending on the solution algorithm / method:
    #   `PowerFlowSolutionFixedPoint`, `PowerFlowSolutionZBus`.
    #   (`PowerFlowSolutionOpenDSS` requires a `ElectricGridModelOpenDSS` instead of `ElectricGridModelDefault`.)
    power_flow_solution = (
        fledge.electric_grid_models.PowerFlowSolutionZBus(
            electric_grid_model,
            der_power_vector_nominal
        )
    )

    # Obtain results (as numpy arrays).
    der_power_vector = pd.Series(power_flow_solution.der_power_vector, index=electric_grid_model.ders)
    node_voltage_vector = pd.Series(power_flow_solution.node_voltage_vector, index=electric_grid_model.nodes)
    node_voltage_vector_magnitude = pd.Series(np.abs(power_flow_solution.node_voltage_vector), index=electric_grid_model.nodes)
    branch_power_vector_1 = pd.Series(power_flow_solution.branch_power_vector_1, index=electric_grid_model.branches)
    branch_power_vector_2 = pd.Series(power_flow_solution.branch_power_vector_2, index=electric_grid_model.branches)
    loss = pd.Series(power_flow_solution.loss, index=['total'])

    # Save results to CSV.
    der_power_vector.to_csv(os.path.join(results_path, f'der_power_vector.csv'))
    node_voltage_vector.to_csv(os.path.join(results_path, f'node_voltage_vector.csv'))
    node_voltage_vector_magnitude.to_csv(os.path.join(results_path, f'node_voltage_vector_magnitude.csv'))
    branch_power_vector_1.to_csv(os.path.join(results_path, f'branch_power_vector_1.csv'))
    branch_power_vector_2.to_csv(os.path.join(results_path, f'branch_power_vector_2.csv'))
    loss.to_csv(os.path.join(results_path, f'loss.csv'))

    # Print results path.
    fledge.utils.launch(results_path)
    print(f"Results are stored in: {results_path}")


if __name__ == '__main__':
    main()
