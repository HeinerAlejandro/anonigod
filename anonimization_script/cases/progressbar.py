import progressbar

from abc import ABC, abstractmethod


class ProgressBarAbstract(ABC):
    abstractmethod
    def render(self):
        pass
    @abstractmethod
    def progress(self):
        pass
    

class ProgressBar(ProgressBarAbstract):
    def __init__(self, steps_count: int):
        self._bar = progressbar.progressbar(steps_count)
    