from typing import Dict, List

import random
import codetiming as ct
from apricopt.solving.blackbox.BlackBoxSolver import BlackBoxSolver

from apricopt_synthesis.blackbox.SynthesisBlackBox import SynthesisBlackBox
from apricopt_synthesis.input import parse_synthesis_config_file
from apricopt_synthesis.blackbox.sbml.SBMLSynthesisBlackBox import SBMLSynthesisBlackBox


def synthesize_therapy_SBML_from_yaml(filename: str):
    synthesis_model, treatment_model, \
        virtual_patients, initial_treatment, \
        exclude_from_initialization, \
        synthesis_horizon, treatment_horizon, \
        random_seed, sim_engine, solver, \
        solver_parameters, num_processes, \
        output_filename = parse_synthesis_config_file(filename)

    black_box: SBMLSynthesisBlackBox = SBMLSynthesisBlackBox(sim_engine, num_processes, synthesis_horizon,
                                                             synthesis_model, treatment_model)
    return synthesize_therapy(black_box, virtual_patients, initial_treatment, exclude_from_initialization, random_seed, solver,
                       solver_parameters)


def synthesize_therapy(black_box: SynthesisBlackBox,
                       virtual_patients: Dict[str, Dict[str, float]],
                       initial_treatment: Dict[str, float],
                       exclude_from_initialization: List[str],
                       random_seed: int, solver: BlackBoxSolver,
                       solver_parameters: list):
    """
    This method performs the personalized synthesis on the given black_box
    :param black_box: An instance of SynthesisBlackBox that represents the treated model.
    :param virtual_patients:
    :param initial_treatment:
    :param exclude_from_initialization:
    :param random_seed:
    :param solver:
    :param solver_parameters:
    :return:
    """
    print("\n\n============ Personalised Therapy Synthesis ===========")
    print(f"Digital Twin size: {len(virtual_patients)}")
    random.seed(random_seed)
    timer = ct.Timer()
    timer.logger = None

    if isinstance(virtual_patients, dict):
        patients_list = []
        for patient_id, patient in virtual_patients.items():
            tmp = dict(patient)
            tmp['id'] = patient_id
            patients_list.append(tmp)
    elif isinstance(virtual_patients, list):
        patients_list = virtual_patients
    else:
        patients_list = virtual_patients

    black_box.set_optimization_parameters_initial_values(initial_treatment)

    black_box.set_digital_twin(patients_list,
                               excluded_parameters_ids={'id', 'admissible', 'init_time'},
                               initialize=True,
                               exclude_from_initialization=exclude_from_initialization)

    print("======== Starting therapy optimisation ========")

    best_therapy, best_value, h_return, n_bb_evals, nb_iters = solver.solve(black_box, solver_parameters,
                                                                            print_bb_evals=True)

    print(f"\n\n====================\nBest Value found in {n_bb_evals} black-box evaluations: {best_value}\n")
    print(f"Best Parameters: {best_therapy}\n====================\n\n")
    return best_therapy, best_value, h_return, n_bb_evals, nb_iters
