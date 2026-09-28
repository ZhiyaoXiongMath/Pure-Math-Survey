"""Typed mathematical dependency graph. Navigation never implies a proof."""
from __future__ import annotations
from .common import SurveyError
from .models import Node
HARD = {'uses_definition', 'proof_input'}

def targets(node: Node, explain: bool = False) -> list[str]:
    kinds = HARD | ({'explained_by'} if explain else set())
    return [edge['target'] for edge in node.meta['links'] if edge['relation'] in kinds]

def detect_cycles(nodes: dict[str, Node]) -> None:
    done, active = set(), []
    def visit(key: str) -> None:
        if key in active:
            trail = active[active.index(key):] + [key]
            raise SurveyError('DEPENDENCY_CYCLE', ' -> '.join(trail), nodes[key].path, key)
        if key in done:
            return
        active.append(key)
        for dep in targets(nodes[key]):
            visit(dep)
        active.pop(); done.add(key)
    for key in nodes:
        visit(key)

def required_closure(nodes: dict[str, Node], seeds: set[str] | list[str], explain: set[str] | None = None) -> set[str]:
    result, todo = set(), list(seeds)
    while todo:
        key = todo.pop()
        if key in result:
            continue
        if key not in nodes:
            raise SurveyError('UNKNOWN_REFERENCE', 'Node required by selection is missing', node_id=key)
        result.add(key)
        todo.extend(targets(nodes[key], key in (explain or set())))
    return result

def topological(nodes: dict[str, Node], selected: set[str]) -> list[str]:
    """Hard prerequisite order. Pedagogical order remains editable in outline."""
    done, order = set(), []
    def visit(key: str) -> None:
        if key in done:
            return
        done.add(key)
        for dep in targets(nodes[key]):
            if dep in selected:
                visit(dep)
        order.append(key)
    for key in sorted(selected):
        visit(key)
    return order

def affected_dependents(nodes: dict[str, Node], changed: set[str], explain: set[str] | None = None) -> set[str]:
    affected = set(changed)
    while True:
        before = len(affected)
        for key, node in nodes.items():
            if set(targets(node, key in (explain or set()))) & affected:
                affected.add(key)
        if before == len(affected):
            return affected - changed
