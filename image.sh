#!/bin/bash
dot -Tps <(./decision_tree.py 1) -o graph1.ps
gv graph1.ps
