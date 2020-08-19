# Reconstructing Broadband Dielectric Properties
This is an analytic model to reconstruct the dielectric properties of a material according to the scattering parameters.

## Background

This is my bachelor thesis with the title: 'Implementation of a Method for Reconstructing Broadband Dielectric Properties'.
The goal of this work is to present a working model for reconstructing the relative permittivity
from the scattering parameters in a broadband frequency range. This is useful for characterizing soil in environmental research.
A simulation for creating such a dataset of scattering parameters is also presented here. This is useful for validating the analytic model and the code.

## Forward Simulation

The forward simulation (forward.py) creates a set of scattering parameters in a selected range according to a selected permittivity. This range and permittivity can be selected by parsing some arguments, but the code already suggests reasonable parameters.

## Inverse Model

The inverse model reconstructs the permittivity from the scattering parameters according to a analytic calculation. Those scattering parameters can be measured by a vector network analyzer for a given material. For testing purposes the scattering parameters can be generated analytically from the forward simulation.

## Contribution

The code and the thesis are written by Jan Zimbelmann.
