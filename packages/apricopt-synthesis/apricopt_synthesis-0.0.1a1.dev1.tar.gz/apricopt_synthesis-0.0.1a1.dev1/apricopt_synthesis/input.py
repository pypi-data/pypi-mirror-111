import json
from typing import Dict, Tuple, Set, List
import petab

from apricopt.IO.data_input import parse_config_file, get_parameter_space, get_objective, get_constraints, \
    get_fast_constraints, get_conditions
from apricopt.model.FastObservable import FastObservable

from apricopt.model.Observable import Observable
from apricopt.model.Parameter import Parameter
from apricopt.simulation.COPASI.COPASIEngine import COPASIEngine
from apricopt.simulation.SimulationEngine import SimulationEngine
from apricopt.solving.blackbox.BlackBoxSolver import BlackBoxSolver
from apricopt.solving.blackbox.MockUp.MockUpSolver import MockUpSolver
from apricopt.solving.blackbox.NOMAD.NOMADSolver import NOMADSolver

from apricopt_synthesis.blackbox.SynthesisModel import SynthesisModel
from apricopt_synthesis.blackbox.TreatmentModel import TreatmentModel


def parse_synthesis_config_file(config_filename: str) -> \
        Tuple[
            SynthesisModel,
            TreatmentModel,
            Dict[str, Dict[str, float]],
            Dict[str, float],
            List[str],
            float, float,
            int, SimulationEngine, BlackBoxSolver,
            List[str], int, str]:
    """
    Builds all objects needed for the personalized synthesis.
    :param config_filename: The name of the YAML file that contains the configuration
    :return:
    """
    data: dict = parse_config_file(config_filename)

    sim_engine: SimulationEngine
    if data['simulator'].lower() == "copasi":
        sim_engine = COPASIEngine()
    else:
        raise ValueError()

    solver: BlackBoxSolver
    if data['solver'].lower() == "nomad":
        solver = NOMADSolver()  # ParallelNOMADSolver()
    elif data['solver'].lower() == "mockup":
        solver = MockUpSolver()
    else:
        raise ValueError()

    synthesis_model: SynthesisModel
    treatment_model: TreatmentModel

    synthesis_model, treatment_model, \
        virtual_patients, initial_treatment, \
        exclude_from_initialization = \
        initialise_model_with_PEtab_files_synthesis(files=data['files'], sim_engine=sim_engine,
                                                    abs_tol_synthesis=data['absolute_tolerance_synthesis'],
                                                    rel_tol_synthesis=data['relative_tolerance_synthesis'],
                                                    abs_tol_treat=data['absolute_tolerance_treatment'],
                                                    rel_tol_treat=data['relative_tolerance_treatment'],
                                                    time_step_synthesis=data['time_step_synthesis'],
                                                    time_step_treat=data['time_step_treatment'])

    synthesis_horizon = float(data['synthesis_horizon'])
    treatment_horizon = float(data['treatment_horizon'])
    solver_parameters = data['solver_parameters']
    random_seed = int(data['random_seed'])
    num_processes = int(data['num_processes'])
    output_filename = data['output_file']

    return synthesis_model, treatment_model, virtual_patients, initial_treatment, exclude_from_initialization, \
        synthesis_horizon, treatment_horizon, \
        random_seed, sim_engine, solver, \
        solver_parameters, num_processes, \
        output_filename


def initialise_model_with_PEtab_files_synthesis(files: Dict[str, str], sim_engine: SimulationEngine,
                                                abs_tol_synthesis: float,
                                                rel_tol_synthesis: float,
                                                abs_tol_treat: float,
                                                rel_tol_treat: float,
                                                time_step_synthesis: float,
                                                time_step_treat: float,
                                                with_virtual_patients=True):
    if 'exclude_from_initialization' in files:
        f = open(files['exclude_from_initialization'])
        exclude_text = f.read()
        f.close()
        exclude_from_initialization = json.loads(exclude_text)
    else:
        exclude_from_initialization = []

    if with_virtual_patients:
        objective_problem = petab.problem.Problem.from_files(sbml_file=files['synthesis_model'],
                                                             parameter_file=files['treatment_parameters'],
                                                             observable_files=files['objective'],
                                                             condition_file=files['virtual_patients'])
    else:
        objective_problem = petab.problem.Problem.from_files(sbml_file=files['synthesis_model'],
                                                             parameter_file=files['treatment_parameters'],
                                                             observable_files=files['objective'])
    if 'efficacy_constraints' in files:
        efficacy_problem = petab.problem.Problem.from_files(sbml_file=files['synthesis_model'],
                                                            parameter_file=files['treatment_parameters'],
                                                            observable_files=files['efficacy_constraints'])
    else:
        efficacy_problem = None

    treatment_problem = petab.problem.Problem.from_files(sbml_file=files['treatment_model'],
                                                         parameter_file=files['treatment_parameters'],
                                                         observable_files=files['treatment_constraints'],
                                                         condition_file=files['initial_treatment'])

    if 'synthesis_observed_outputs' in files:
        f = open(files['synthesis_observed_outputs'])
        observed_outputs_text = f.read()
        f.close()
        synthesis_observed_outputs = json.loads(observed_outputs_text)
    else:
        synthesis_observed_outputs = None

    # The parameter space is the space of treatment parameters
    parameter_space: Set[Parameter] = get_parameter_space(objective_problem.parameter_df)
    objective: Observable = get_objective(objective_problem.observable_df)
    if efficacy_problem:
        efficacy_constraints: Set[Observable] = get_constraints(efficacy_problem.observable_df)
    else:
        efficacy_constraints: Set[Observable] = set()

    # TODO For now, we only use fast constraints for the treatment. Will be changed later. (It is still correct)
    # treatment_constraints: Set[Observable] = get_constraints(constr_problem.observable_df)
    treatment_fast_constraints: Set[FastObservable] = get_fast_constraints(treatment_problem.observable_df)

    virtual_patients: Dict[str, Dict[str, float]] = get_conditions(
        objective_problem.condition_df) if with_virtual_patients else dict()
    initial_treatment: Dict[str, float] = \
        [treat_params for treat_id, treat_params in get_conditions(treatment_problem.condition_df).items()][0]

    synthesis_model: SynthesisModel = SynthesisModel(sim_engine, files['synthesis_model'],
                                                     abs_tol_synthesis, rel_tol_synthesis, time_step_synthesis,
                                                     observed_outputs=synthesis_observed_outputs)
    synthesis_model.set_parameter_space(parameter_space)
    synthesis_model.objective = objective

    if efficacy_constraints:
        synthesis_model.constraints = efficacy_constraints

    treatment_model: TreatmentModel = TreatmentModel(sim_engine, files['treatment_model'],
                                                     abs_tol_treat, rel_tol_treat, time_step_treat)
    treatment_model.set_parameter_space(parameter_space)
    treatment_model.fast_constraints = treatment_fast_constraints
    # treatment_model.objective = objective
    # treatment_model.constraints = treatment_constraints

    return synthesis_model, treatment_model, \
        virtual_patients, initial_treatment, \
        exclude_from_initialization
