from typing import List, Optional, Any, Dict

from checkov.common.graph.checks_infra.enums import Operators
from checkov.terraform.checks_infra.solvers.attribute_solvers.base_attribute_solver import BaseAttributeSolver


class WithinAttributeSolver(BaseAttributeSolver):
    operator = Operators.WITHIN

    def __init__(self, resource_types: List[str], attribute: Optional[str], value: Any) -> None:
        super().__init__(resource_types=resource_types, attribute=attribute, value=value)

    def _get_operation(self, vertex: Dict[str, Any], attribute: Optional[str]) -> bool:
        return vertex.get(attribute) in self.value
