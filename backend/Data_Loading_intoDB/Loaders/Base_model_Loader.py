# this would be a base common class for loading data, which can then be seperately used for different loading sources

from abc import ABC, abstractmethod


class BaseDataLoader(ABC):
    @abstractmethod
    def load(self):
        pass