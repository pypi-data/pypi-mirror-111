from typing import List
from send_handler_interface import FormalProgressInterface

class ProgressReport:
    def __init__(self, step_message: str, send_handler: FormalProgressInterface, steps: int = 0):
        self.step_message = step_message
        self.steps = steps
        self.send_handler = send_handler
        self.completed = False
        self.children: List[ProgressReport] = []

        if not send_handler.has_root():
            # this is the first report for the given send handler
            # so it automatically becomes the root report
            send_handler.set_root_progress_report(self)

    def complete(self):
        self.completed = True
        # re-submit the now completed report
        self.send_handler.submit()

    def create_subreport(self, step_message: str, steps: int = 0) -> 'ProgressReport':
        child = ProgressReport(step_message=step_message, send_handler=self.send_handler, steps=steps)
        self.children.append(child)
        self.send_handler.submit()
        return child

