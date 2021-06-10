"""Example script for setting up and solving an electric grid optimal operation problem."""

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

    # Obtain data.
    scenario_data = fledge.data_interface.ScenarioData(scenario_name)
    price_data = fledge.data_interface.PriceData(scenario_name)

    # Obtain models.
    linear_electric_grid_model = fledge.electric_grid_models.LinearElectricGridModelGlobal(scenario_name)
    der_model_set = fledge.der_models.DERModelSet(scenario_name)

    # Instantiate optimization problem.
    optimization_problem = fledge.utils.OptimizationProblem()

    # Define optimization variables.
    linear_electric_grid_model.define_optimization_variables(optimization_problem)
    der_model_set.define_optimization_variables(optimization_problem)

    # Define constraints.
    linear_electric_grid_model.define_optimization_constraints(optimization_problem)
    der_model_set.define_optimization_constraints(optimization_problem)

    # Define objective.
    linear_electric_grid_model.define_optimization_objective(
        optimization_problem,
        price_data
    )
    der_model_set.define_optimization_objective(
        optimization_problem,
        price_data
    )

    # Solve optimization problem.
    optimization_problem.solve()

    # Obtain results.
    results = fledge.problems.Results()
    results.update(linear_electric_grid_model.get_optimization_results(optimization_problem))
    results.update(der_model_set.get_optimization_results(optimization_problem))

    # Print results.
    print(results)

    # Store results to CSV.
    results.save(results_path)

    # Print results path.
    fledge.utils.launch(results_path)
    print(f"Results are stored in: {results_path}")


if __name__ == '__main__':
    main()
