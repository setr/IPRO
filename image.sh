#!/bin/bash
dot -Tps <(./decision_tree.py) -o graph1.ps
gv graph1.ps
