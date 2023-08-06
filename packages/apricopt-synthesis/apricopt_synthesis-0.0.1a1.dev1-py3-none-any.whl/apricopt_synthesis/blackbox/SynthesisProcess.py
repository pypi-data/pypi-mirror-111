import math
import multiprocessing as mp
import os
import time
from typing import List, Dict

from apricopt.simulation.SimulationEngine import SimulationEngine

from apricopt_synthesis.blackbox.SynthesisModel import SynthesisModel


class SynthesisProcess(mp.Process):

    def __init__(self, vp_models: List[SynthesisModel], sim_engine: SimulationEngine, time_horizon: float) -> None:
        super(SynthesisProcess, self).__init__()
        self.vp_models = vp_models
        self.sim_engine = sim_engine
        self.time_horizon = time_horizon
        self.trajectories: List[Dict[str, float]] = []
        self.queue = mp.Queue()

    def set_treatment(self, treatment: Dict[str, float]) -> None:
        self.trajectories = []
        for vp in self.vp_models:
            vp.set_params(treatment)

    def run(self) -> None:
        tmp_trajectories = []
        process_start = time.perf_counter()
        for pat in self.vp_models:
            obj = {}
            sim_start = time.perf_counter()
            try:
                trajectory = self.sim_engine.simulate_trajectory(pat, self.time_horizon)
                self.print_information(trajectory, pat.pat_id)
                obj = pat.evaluate_constraints(trajectory)
                trajectory.pop('time')
                self.efficacy(trajectory, obj)
                for obs_id, obj_val in trajectory.items():
                    if not math.isnan(obj_val[-1]):
                        obj[obs_id] = obj_val[-1]
                    else:
                        obj[pat.objective.id] = pat.objective.upper_bound
                        break
            except:
                obj[pat.objective.id] = pat.objective.upper_bound
            print(f"\t\t\t\nPatient {pat.pat_id} simulation time: {time.perf_counter() - sim_start:.2f} seconds",
                  flush=True)

            tmp_trajectories.append(obj)

        print(f"\n\t\t\nProcess execution time: {time.perf_counter() - process_start:.2f} seconds", flush=True)
        self.queue.put(tmp_trajectories.copy())
        # for traj in tmp_trajectories:
        #    self.queue.put(traj, block=False)

    def start(self) -> None:
        # self._check_closed()
        assert self._parent_pid == os.getpid(), \
            'can only start a process object created by current process'
        # assert not _current_process._config.get('daemon'), \
        #        'daemonic processes are not allowed to have children'

        self._popen = self._Popen(self)
        self._sentinel = self._popen.sentinel

    def get_results(self) -> List[Dict[str, float]]:
        self.trajectories = self.queue.get()

        # while not self.queue.empty():
        #    self.trajectories.append(self.queue.get(False))

        return self.trajectories

    # TODO: temporary hard-coded
    def efficacy(self, trajectory, results):
        tumour_diameter = max(0.001, trajectory['tumour_diameter'][-1])
        initial_tumour_diameter = trajectory['tumour_diameter'][0]
        efficacy = min(500.0, tumour_diameter * (tumour_diameter / initial_tumour_diameter))
        results['inefficacy'] = efficacy

    def print_information(self, trajectory, pat_id):
        print(f"\tPatient id: {pat_id}\n\t\tInitial tumour diameter: {trajectory['tumour_diameter'][0]:.2f} mm")


