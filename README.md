# Quantum Teleportation Coexisting with Classical Communications – Task Replication

> Quantum teleportation coexisting with high-rate classical data traffic in optical fibers
> J. M. Thomas et al., arXiv:2404.10738v4
> https://arxiv.org/abs/2404.10738

This repository contains a complete task designed for the Professional Operation Agent Evaluation project, which replicates key calculations from the paper. 

The task demonstrates the use of SCP (Scientific Context Protocol) and MCP (Model Context Protocol) tools to perform scientific computations in the domain of quantum optics.

## Repository Structure
├── README.md
├── .gitignore
├── generate\_all\_results.py # Python script to generate all outputs
├── phys-optics-20250320-abcd.task.json # Task definition (SCP/MCP instructions)
├── phys-optics-20250320-abcd.trace.json # Execution trajectory (thoughts + tool calls)
├── input\_data/
│ └── paper.pdf # Original paper (arXiv version)
└── others/
└── eval\_scripts/
└── validate\_results.py # Self-validation script

##  How to Run
1. Clone the repository

2. Install dependencies
pip install numpy matplotlib

3. Generate all results
python generate\_all\_results.py

4. Validate the outputs (optional)
python others/eval\_scripts/validate\_results.py

##  Task Overview

The task mimics a real research workflow:

1.Extract experimental parameters from the paper PDF.

2. Compute fundamental optical quantities (photon energy, numerical aperture, reflectance, photon flux).

3.Model spontaneous Raman scattering (SpRS) noise and generate a power‑dependent curve.

4.Produce a structured report and JSON summary.

All calculations are performed using SCP tools (Optics-Calculator) and MCP tools (Python-Code-Executor, Filesystem-MCP), with a clear separation of concerns (SCP > MCP).

##  License
This project is released under the MIT License.
The original paper is subject to its own copyright.



