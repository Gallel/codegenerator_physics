"""Ontology loading with a per-process cache."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Any

import owlready2
from owlready2 import get_ontology

log = logging.getLogger(__name__)

# Cache keyed by the resolved absolute path so that relative and absolute
# spellings of the same file map to one entry.
_ONTOLOGY_CACHE: Dict[str, Any] = {}
_ONTO_PATH_REGISTERED: set = set()


def load_ontology(path):
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError("Ontology not found at: " + str(p))

    key = p.as_posix()
    cached = _ONTOLOGY_CACHE.get(key)
    if cached is not None:
        return cached

    parentDir = p.parent.as_posix()
    if parentDir not in _ONTO_PATH_REGISTERED:
        if parentDir not in owlready2.onto_path:
            owlready2.onto_path.append(parentDir)
        _ONTO_PATH_REGISTERED.add(parentDir)

    print("[INFO] Loading ontology from: " + key);
    onto = get_ontology(key).load()
    _ONTOLOGY_CACHE[key] = onto
    return onto
