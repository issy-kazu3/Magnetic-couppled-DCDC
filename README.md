# Magnetic-couppled-DCDC
Magnetic‑coupled DC/DC converter analysis using Maxwell 3D and Python. Generates current‑dependent inductance maps (L1, L2, M) and computes ripple &amp; flux waveforms using leakage‑flux reactors.
# Overview
This project provides a complete workflow for analyzing magnetic‑coupled DC/DC converters that use leakage‑flux reactors.
Conventional linear inductor models cannot be used due to strong current‑dependent inductance behavior, so a 3D FEM‑based inductance map is generated and used for ripple/flux calculation.

<img width="156" height="152" alt="inductor" src="https://github.com/user-attachments/assets/915d4e28-277c-40b4-85b2-137171a9bc19" />
<img width="266" height="134" alt="dcdc" src="https://github.com/user-attachments/assets/3b74cd42-bfb7-4134-8c30-a0a6ac855e8a" />


# Features
Magnetic‑coupled reactor modeling

Leakage‑flux based voltage generation

DC flux cancellation with opposite winding polarity

Maxwell 3D parametric simulation (VBS)

Python DOE automation for inductance map generation

Ripple current & flux waveform calculation

Loss estimation (iron & copper)

# Workflow
  ## Maxwell 3D

    Parametric model

    Current sweep (I1, I2)

    Export L1(I1,I2), L2(I1,I2), M(I1,I2)

  ## Python DOE

      Batch execution of Maxwell

      CSV processing

      Interpolation & map construction

  ## Python Ripple Calculation

      Ripple current

      Flux waveform

      Loss estimation

# Repository Structure
core/ — Ripple calculation logic

maxwell/ — VBS scripts & Python interface

tools/ — CSV utilities, plotting

docs/ — Technical documentation

examples/ — Sample data

# Documentation
Full technical explanation is available in the docs:

Overview

Maxwell Workflow

Inductance Map Theory

Ripple Calculation

# License
MIT License (or your preferred license)
