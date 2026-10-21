"""Mechanical definition and route dependencies, never mathematical certification."""
from __future__ import annotations
from .common import SurveyError
from .models import Node


def targets(node: Node, explain: bool = False) -> list[str]:
    return node.meta['definition_refs']


def route_inputs(route: dict) -> set[str]:
    return {key for group in route['premise_sets'] for key in group['nodes']}


def detect_cycles(nodes: dict[str, Node], routes: list[dict] = ()) -> None:
    edges={k:set(targets(n)) for k,n in nodes.items()}
    for route in routes: edges[route['target']].update(route_inputs(route))
    done,active=set(),[]
    def visit(key):
        if key in active:
            raise SurveyError('DEPENDENCY_CYCLE',' -> '.join(active[active.index(key):]+[key]),nodes[key].path,key)
        if key in done:return
        active.append(key)
        for dep in sorted(edges[key]):visit(dep)
        active.pop();done.add(key)
    for key in nodes:visit(key)


def required_closure(nodes: dict[str, Node], seeds, explain=None) -> set[str]:
    found,todo=set(),list(seeds)
    while todo:
        key=todo.pop()
        if key in found:continue
        if key not in nodes:raise SurveyError('UNKNOWN_REFERENCE','Required node is missing',node_id=key)
        found.add(key);todo.extend(targets(nodes[key]))
    return found


def topological(nodes: dict[str, Node], selected: set[str]) -> list[str]:
    done,order=set(),[]
    def visit(key):
        if key in done:return
        done.add(key)
        for dep in targets(nodes[key]):
            if dep in selected:visit(dep)
        order.append(key)
    for key in sorted(selected):visit(key)
    return order


def affected_dependents(nodes: dict[str, Node], changed: set[str], routes=()) -> set[str]:
    affected=set(changed)
    edges={k:set(targets(n)) for k,n in nodes.items()}
    for route in routes:edges[route['target']].update(route_inputs(route))
    while True:
        before=len(affected)
        for key,node in nodes.items():
            if edges[key] & affected:affected.add(key)
        if len(affected)==before:return affected-changed
