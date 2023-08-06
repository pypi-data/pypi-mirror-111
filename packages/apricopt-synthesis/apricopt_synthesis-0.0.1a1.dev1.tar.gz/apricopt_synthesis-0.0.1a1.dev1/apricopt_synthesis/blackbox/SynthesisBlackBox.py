from abc import ABC, abstractmethod
from typing import List, Dict, Set

from apricopt.solving.blackbox.BlackBox import BlackBox


class SynthesisBlackBox(BlackBox, ABC):

    @abstractmethod
    def set_digital_twin(self, digital_twin: List[Dict[str, float]],
                         excluded_parameters_ids: Set[str],
                         initialize=False, exclude_from_initialization=None,
                         init_time_parameter_id="init_time") -> None:
        pass
