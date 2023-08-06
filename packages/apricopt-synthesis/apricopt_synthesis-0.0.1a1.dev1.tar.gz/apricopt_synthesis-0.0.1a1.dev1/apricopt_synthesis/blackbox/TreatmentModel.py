from typing import List, Dict

from apricopt.model import Parameter
from apricopt.model.Model import Model
import numpy as np


class TreatmentModel(Model):
    def __init__(self, sim_engine, model_filename: str, abs_tol: float, rel_tol: float, time_step: float,
                 observed_outputs: List[str] = None):
        super().__init__(sim_engine, model_filename, abs_tol, rel_tol, time_step, observed_outputs=observed_outputs)

    def is_admissible(self, params: Dict[str, float]) -> bool:
        constraint_values: Dict[str, float] = self.evaluate_fast_constraints(params)
        return all(constraint_values[constraint_id] <= 0 for constraint_id in constraint_values.keys())

    def sample_treatment(self):
        parameters: List[Parameter] = list(self.parameters.values())
        parameters.sort(key=lambda x: x.id)
        sample = np.random.rand(len(parameters))
        sampled_therapy: Dict[str, float] = dict()
        for i in range(len(parameters)):
            param = parameters[i]
            if param.distribution == 'uniform':
                sampled_therapy[param.id] = \
                    round(param.lower_bound + (
                            param.upper_bound - param.lower_bound) * sample[i])
        return sampled_therapy
