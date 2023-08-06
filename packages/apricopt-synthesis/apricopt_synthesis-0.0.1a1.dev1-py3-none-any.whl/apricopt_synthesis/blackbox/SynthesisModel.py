from typing import List, Set, Dict

from apricopt.model.Model import Model, Observable


class SynthesisModel(Model):
    def __init__(self, sim_engine, model_filename: str, abs_tol: float, rel_tol: float, time_step: float,
                 observed_outputs: List[str] = None):
        super().__init__(sim_engine, model_filename, abs_tol, rel_tol, time_step, observed_outputs=observed_outputs)
        self.initialization_constraints: Set[Observable] = set()
        self.admissibility_constraints: Set[Observable] = set()
        self.pat_id = None

    def build_zero_sim_output(self) -> Dict[str, float]:
        sim_output = super().build_zero_sim_output()
        for admissibility_constraint in self.admissibility_constraints:
            sim_output[admissibility_constraint.id] = admissibility_constraint.upper_bound

        for initialisation_constraint in self.initialization_constraints:
            sim_output[initialisation_constraint.id] = initialisation_constraint.upper_bound
        return sim_output

    def get_observables_ids(self) -> Set[str]:
        if not self.cached_ids:
            self.cached_ids: Set[str] = set()
            if self.objective:
                self.cached_ids.add(self.objective.id)

            for constraint in self.constraints:
                self.cached_ids.add(constraint.id)

            for admissibility_constraint in self.admissibility_constraints:
                self.cached_ids.add(admissibility_constraint.id)

            for initialisation_constraint in self.initialization_constraints:
                self.cached_ids.add(initialisation_constraint.id)
            '''
            for response_constraint in self.response_constraints:
                self.cached_ids.add(response_constraint.id)
            '''
        return self.cached_ids

    def evaluate_admissibility_constraints(self, trajectory) -> Dict[str, float]:
        result: Dict[str, float] = dict()
        full_trajectory: Dict[str, List[float]] = self.complete_trajectory(trajectory)
        for adm_obs in self.admissibility_constraints:
            result[adm_obs.id] = adm_obs.evaluate(full_trajectory)
        return result

    def evaluate_initialization_constraints(self, trajectory) -> Dict[str, float]:
        result: Dict[str, float] = dict()
        full_trajectory: Dict[str, List[float]] = self.complete_trajectory(trajectory)
        for init_obs in self.initialization_constraints:
            result[init_obs.id] = init_obs.evaluate(full_trajectory)
        return result

    def evaluate_constraints(self, trajectory: Dict[str, List[float]]) -> Dict[str, float]:
        full_trajectory: Dict[str, List[float]] = self.complete_trajectory(trajectory)
        result: Dict[str, float] = dict()
        if self.objective:
            result[self.objective.id] = self.objective.evaluate(full_trajectory)
        for constraint in self.constraints:
            result[constraint.id] = constraint.evaluate(full_trajectory)
        for ac in self.admissibility_constraints:
            result[ac.id] = ac.evaluate(full_trajectory)
        for ic in self.initialization_constraints:
            result[ic.id] = ic.evaluate(full_trajectory)
        return result
