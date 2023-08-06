"""
This file is part of Apricopt.

Apricopt is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Apricopt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Apricopt.  If not, see <http://www.gnu.org/licenses/>.

Copyright (C) 2020-2021 Marco Esposito, Leonardo Picchiami.
"""

import math
import time
from typing import List, Dict, Tuple
import codetiming as ct

from apricopt.simulation.SimulationEngine import SimulationEngine

from apricopt_synthesis.blackbox.SynthesisBlackBox import SynthesisBlackBox
from apricopt_synthesis.blackbox.SynthesisModel import SynthesisModel
from apricopt_synthesis.blackbox.SynthesisProcess import SynthesisProcess
from apricopt_synthesis.blackbox.TreatmentModel import TreatmentModel
from apricopt_synthesis.blackbox.sbml.DigitalTwinNotSetError import DigitalTwinNotSetError


class SBMLSynthesisBlackBox(SynthesisBlackBox):

    def __init__(self, sim_engine: SimulationEngine, num_processes: int, horizon: float,
                 synthesis_model: SynthesisModel, treatment_model: TreatmentModel
                 ):
        self.sim_engine: SimulationEngine = sim_engine
        self.num_processes: int = num_processes
        self.horizon = horizon
        self.synthesis_model = synthesis_model
        self.treatment_model = treatment_model
        self.digital_twin: List[SynthesisModel] = []

        self.__parameters_ids, self.__parameters_lower_bounds, self.__parameters_upper_bounds, \
            self.__initial_values, self.__granularity = \
            self._cache_parameters_info()

        self.__extreme_constraints_ids, self.__progressive_constraints_ids = self._cache_constraints_info()

        self.start_time = time.perf_counter()
        # ~ End init

    def set_digital_twin(self, digital_twin: List[Dict[str, float]],
                         excluded_parameters_ids: None,
                         initialize=False, exclude_from_initialization=None,
                         init_time_parameter_id="init_time") -> None:
        """
        Creates a SynthesisModel instance for each patient in the digital twin.
        If initialize=True, initializes all models simulating them.
        The simulation time for the initialization is assumed to be a parameter of each VP with id
        init_time_parameter_id. This parameter defaults to "init_time".
        :param excluded_parameters_ids: A list of strings representing virtual patient parameters that will be ignored
        (i.e., that do not directly define the virtual patient, but give some information on it such as admissibility).
        :param digital_twin: A list of str->float dictionaries that represents the digital twin, i.e. virtual patients,
        each of which is an assignment to the model parameters.
        :param initialize: True if the model has to be initialized before the synthesis starts, False otherwise.
        :param exclude_from_initialization: A list of strings representing model values that must be excluded from the
        initialization.
        :param init_time_parameter_id: The identifier of the virtual patient parameter that represents the time required
        to initialize it.
        :return: None
        """
        if excluded_parameters_ids is None:
            excluded_parameters_ids = set()  # TODO should be {'id', 'admissible', 'init_time'}
        timer = ct.Timer()
        timer.logger = None

        print("Initializing set of VPs to parallel computation...")
        timer.start()
        for vp in digital_twin:
            copied_synthesis_model = self.synthesis_model.copy()
            vp_params = {param_name: vp[param_name] for param_name in vp if
                  param_name not in excluded_parameters_ids}
            copied_synthesis_model.set_fixed_params(vp_params)

            copied_synthesis_model.pat_id = int(float(vp['id']))
            if initialize:
                init_time = vp[init_time_parameter_id]
                self.sim_engine.simulate_and_set(copied_synthesis_model, init_time,
                                                 exclude=exclude_from_initialization,
                                                 evaluate_constraints=False)
            self.digital_twin.append(copied_synthesis_model)
        print(f"Initialisation time of parallel computation: {timer.stop():.2f} sec")

        # Once the digital twin has been set, we can initialize the process pool
        self.__processes_pool = self._initialize_synthesis_processes(self.num_processes, self.horizon)

    def evaluate(self, parameters: Dict[str, float]) -> Dict[str, float]:
        if not self.digital_twin:
            raise DigitalTwinNotSetError("Before evaluating the black box, you must set the digital twin, using the "
                                         "method set_digital_twin(...)")
        if not self.treatment_model.is_admissible(parameters):
            objective: Dict[str, float] = self.synthesis_model.build_zero_sim_output()
        else:
            eval_start = time.perf_counter()

            for process in self.__processes_pool:
                process.set_treatment(parameters)

            for process in self.__processes_pool:
                process.start()

            tmp_data = [list() for _ in range(len(self.__processes_pool))]
            for i in range(len(self.__processes_pool)):
                tmp_data[i] = self.__processes_pool[i].get_results()
                self.__processes_pool[i].join()

            all_objective = []
            for data in tmp_data:
                all_objective += data

            if self.any_simulation_failed(all_objective):
                objective = self.synthesis_model.build_zero_sim_output()
            else:
                objective = self.compute_objective_expected_value(all_objective)
                self.print_statistics(all_objective, eval_start, self.start_time)

        return dict(objective, **self.treatment_model.evaluate_fast_constraints(parameters))

    def set_optimization_parameters_initial_values(self, param_values: Dict[str, float]) -> None:
        for param_id, param_value in param_values.items():
            self.__initial_values[param_id] = param_value
        self.treatment_model.set_parameters_nominal_values(param_values)

    def any_simulation_failed(self, all_trejectories: List[dict]) -> bool:
        for trajectory in all_trejectories:
            if trajectory[self.synthesis_model.objective.id] == self.synthesis_model.objective.upper_bound:
                return True
        return False

    def compute_objective_expected_value(self, objective_values: List[Dict[str, float]]) -> \
            Dict[str, float]:
        expected_value = 0
        for val in objective_values:
            expected_value += val[self.synthesis_model.objective.id]

        obj = dict()
        obj[self.synthesis_model.objective.id] = expected_value / len(objective_values)
        return obj

    def print_statistics(self, values: List[Dict[str, float]], eval_start: float,
                         opt_start: float) -> None:
        expected_val_dict = self.expected_values(values)
        variance_dict = self.variance(values)
        standard_deviation_dict = self.standard_deviation(values)
        data_ids = list(values[0].keys())
        for val in sorted(data_ids):
            # TODO: temporary hard-coded
            if val != 'total_drugs':
                print(f"\tMean {val}: {expected_val_dict[val]:.2f}\t",
                      f"Variance {val}: {variance_dict[val]:.2f}\t",
                      f"Standard deviation {val}: {standard_deviation_dict[val]:.2f}", sep='', flush=True)
        print(f"\nBlackbox evaluation time: {time.perf_counter() - eval_start:.2f} seconds", flush=True)
        print(f"Current optimisation time: {self.to_hms(time.perf_counter() - opt_start)}\n\n", flush=True)

    @staticmethod
    def to_hms(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return '{} hours {:0>2} minutes {:0>2.2f} seconds'.format(h, m, s)

    def expected_values(self, values: List[Dict[str, float]]) -> Dict[str, float]:
        all_data_id = list(values[0].keys())
        results = dict()
        for data_id in all_data_id:
            expected = 0
            for val in values:
                expected += val[data_id]
            results[data_id] = expected / len(values)

        return results

    def variance(self, values: List[Dict[str, float]]) -> Dict[str, float]:
        mean_dict = self.expected_values(values)
        variance_dict = dict()
        for data_id in mean_dict.keys():
            variance_dict[data_id] = sum(
                [(abs(val[data_id] - mean_dict[data_id])) ** 2 for val in values]) / len(values)
        return variance_dict

    def standard_deviation(self, values: List[Dict[str, float]]) -> Dict[str, float]:
        variance_dict = self.variance(values)
        std_dict = dict()
        for data_id, value in variance_dict.items():
            std_dict[data_id] = math.sqrt(value)
        return std_dict

    def get_optimization_parameters_number(self) -> int:
        return len(self.treatment_model.parameters)

    def get_optimization_parameters_ids(self) -> List[str]:
        return self.__parameters_ids

    def _cache_parameters_info(self) -> Tuple[List[str], Dict[str, float], Dict[str, float], Dict[str, float],
                                              Dict[str, float]]:
        lower_bounds: Dict[str, float] = {}
        upper_bounds: Dict[str, float] = {}
        initial_values: Dict[str, float] = {}
        granularity: Dict[str, float] = {}

        params_ids: List[str] = [p_id for p_id in self.treatment_model.parameters]
        params_ids.sort()

        for parameter_id, parameter in self.treatment_model.parameters.items():
            lower_bounds[parameter_id] = parameter.lower_bound
            upper_bounds[parameter_id] = parameter.upper_bound
            initial_values[parameter_id] = parameter.nominal_value
            granularity[parameter_id] = parameter.granularity

        return params_ids, lower_bounds, upper_bounds, initial_values, granularity

    def get_optimization_parameter_lower_bound(self, param_id) -> float:
        return self.__parameters_lower_bounds[param_id]

    def get_optimization_parameter_upper_bound(self, param_id) -> float:
        return self.__parameters_upper_bounds[param_id]

    def get_optimization_parameter_initial_value(self, param_id) -> float:
        return self.__initial_values[param_id]

    def get_optimization_parameter_granularity(self, param_id) -> float:
        return self.__granularity[param_id]

    def get_extreme_barrier_constraints_number(self) -> int:
        return len(self.treatment_model.fast_constraints) + len(self.treatment_model.constraints)

    def get_progressive_barrier_constraints_number(self) -> int:
        return len(self.synthesis_model.constraints) + len(self.synthesis_model.fast_constraints)

    def _cache_constraints_info(self) -> Tuple[List[str], List[str]]:
        extreme_ids: List[str] = []
        progressive_ids: List[str] = []

        for treat_fast_cons in self.treatment_model.fast_constraints:
            extreme_ids.append(treat_fast_cons.id)
        for treat_cons in self.treatment_model.constraints:
            extreme_ids.append(treat_cons.id)
        extreme_ids.sort()

        for fast_cons in self.synthesis_model.fast_constraints:
            progressive_ids.append(fast_cons.id)
        for constraint in self.synthesis_model.constraints:
            progressive_ids.append(constraint.id)
        progressive_ids.sort()

        return extreme_ids, progressive_ids

    def get_extreme_barrier_constraints_ids(self) -> List[str]:
        return self.__extreme_constraints_ids

    def get_progressive_barrier_constraints_ids(self) -> List[str]:
        return self.__progressive_constraints_ids

    def get_objective_id(self) -> str:
        return self.synthesis_model.objective.id

    def get_objective_upper_bound(self) -> float:
        return self.synthesis_model.objective.upper_bound

    @staticmethod
    def get_raisable_exception_type():
        return Exception

    def _initialize_synthesis_processes(self, num_processes: int, horizon: float) -> List[SynthesisProcess]:
        """
        This function configures all processes to simulate:
            - splits the digital twin over processes
            - set the current treatment
        """

        split = len(self.digital_twin) // num_processes

        all_sub_list: List[List[SynthesisModel]] = [
            self.digital_twin[i * split: (i + 1) * split]
            for i in range(num_processes)]

        if num_processes * split < len(self.digital_twin):
            rest = len(self.digital_twin) - num_processes * split
            for i in range(rest):
                all_sub_list[i].append(self.digital_twin[num_processes * split + i])

        processes_pool: List[SynthesisProcess] = [SynthesisProcess(all_sub_list[i], self.sim_engine, horizon)
                                                  for i in range(num_processes)]

        return processes_pool

    def finalize(self):
        for process in self.__processes_pool:
            process.terminate()
