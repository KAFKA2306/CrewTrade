from typing import Type, Dict
from .base import BaseUseCase, UseCaseConfig


class UseCaseRegistry:
    def __init__(self) -> None:
        self._registry: Dict[str, Type[BaseUseCase]] = {}
        self._config_registry: Dict[str, Type[UseCaseConfig]] = {}

    def register(self, name: str, cls: Type[BaseUseCase], config_model: Type[UseCaseConfig]) -> None:
        self._registry[name] = cls
        self._config_registry[name] = config_model

    def get(self, name: str) -> Type[BaseUseCase]:
        return self._registry[name]

    def get_config_model(self, name: str) -> Type[UseCaseConfig]:
        return self._config_registry[name]


_use_case_registry = UseCaseRegistry()


def register_use_case(name: str, cls: Type[BaseUseCase], config_model: Type[UseCaseConfig]) -> None:
    _use_case_registry.register(name, cls, config_model)


def get_use_case_class(name: str) -> Type[BaseUseCase]:
    return _use_case_registry.get(name)


def get_use_case_config_model(name: str) -> Type[UseCaseConfig]:
    return _use_case_registry.get_config_model(name)
