import abc
import json
from progress_report import ProgressReport

def report_to_json(report: 'ProgressReport') -> dict:
    return {
        'step_message': report.step_message,
        'steps': report.steps,
        'completed': report.completed,
        'children': [report_to_json(child) for child in report.children]
    }


class FormalProgressInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        self.__root_progress = None

    def set_root_progress_report(self, progress_report_root: ProgressReport):
        self.__root_progress = progress_report_root
        self.submit()

    def has_root(self) -> bool:
        return self.__root_progress is not None

    def submit(self):
        if self.__root_progress:
            self.send(json.dumps(report_to_json(self.__root_progress)))

    def get_data(self):
        return report_to_json(self.__root_progress)

    @abc.abstractmethod
    def send(self, progress_json: str):
        pass


