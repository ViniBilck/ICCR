# ICCR - Initial Configuration to Collision Route

This README provides an overview of the `iccr.py` code, which is designed to perform calculations related to galaxy collisions. The code is written in Python and requires the following dependencies: `numpy`, `tables`, and `scipy`.

## Table of Contents
- [Introduction](#introduction)
- [Class: Collision](#class-collision)
- [Methods](#methods)
  - [initial_orbit](#initial_orbit)
  - [get_mass](#get_mass)
  - [get_particles](#get_particles)
  - [get_numparts](#get_numparts)
  - [do_rotation](#do_rotation)
  - [initial_condition_file](#initial_condition_file)

## Introduction
The `iccr.py` code provides functionality to analyze and simulate galaxy collisions. It calculates initial orbits, retrieves mass information, manages particle data, performs rotations, and generates initial condition files for further simulations.

## Class: Collision
The `Collision` class represents a galaxy collision and provides methods to perform various calculations and operations on the galaxy data.

### Initialization
```python
collision = Collision(galaxyname1: str, galaxyname2: str)
```
- `galaxyname1` (str): Path to the HDF5 file containing the data for the first galaxy.
- `galaxyname2` (str): Path to the HDF5 file containing the data for the second galaxy.

### Attributes
- `galaxyname1` (str): Path to the HDF5 file containing the data for the first galaxy.
- `galaxyname2` (str): Path to the HDF5 file containing the data for the second galaxy.
- `parttypes_in_hdf5` (list): List of particle types in the HDF5 file.
- `properties_in_hdf5` (list): List of properties available for each particle type.

## Methods

### initial_orbit
```python
initial_orbit(m1, m2, pericenter, escape_velocity=None)
```
Calculates the initial orbital conditions for a galaxy collision.

- `m1` (float): Mass of the first galaxy.
- `m2` (float): Mass of the second galaxy.
- `pericenter` (float): Pericenter distance of the orbit.
- `escape_velocity` (float, optional): Escape velocity. If not provided, it will be calculated based on the pericenter distance and masses.

Returns a dictionary with the following keys:
- `Coord_G1` (list): Initial coordinates of the first galaxy.
- `Coord_G2` (list): Initial coordinates of the second galaxy.
- `Velocities_G1` (list): Initial velocities of the first galaxy.
- `Velocities_G2` (list): Initial velocities of the second galaxy.

### get_mass
```python
get_mass()
```
Retrieves the total mass of the galaxies.

Returns a list with two elements:
- Total mass of the first galaxy.
- Total mass of the second galaxy.

### get_particles
```python
get_particles()
```
Calculates the cumulative number of particles for each particle type in both galaxies.

Returns a list with the cumulative number of particles for each particle type.

### get_numparts
```python
get_numparts()
```
Retrieves the total number of particles for each particle type in both galaxies.

Returns a list with the total number of particles for each particle type.

### do_rotation
```python
do_rotation(which_galaxy: int, rotation_sequence: str, angles: list)
```
Applies rotation to the coordinates and velocities of a galaxy.

- `which_galaxy` (int): Indicates which galaxy to rotate (0 for the

 first galaxy, 1 for the second galaxy).
- `rotation_sequence` (str): Rotation sequence, e.g., 'xyz', 'zxz'.
- `angles` (list): List of angles for the rotation in degrees.

### initial_condition_file
```python
initial_condition_file(pericenter, escape_velocity=None)
```
Generates an initial condition file for further simulations.

- `pericenter` (float): Pericenter distance of the orbit.
- `escape_velocity` (float, optional): Escape velocity. If not provided, it will be calculated based on the pericenter distance and masses.

The function creates a new HDF5 file named "collision_file" and populates it with the necessary data from the original galaxy data files.

## Conclusion
The `iccr.py` code provides a set of methods to perform calculations and operations related to galaxy collisions. By utilizing these methods, you can analyze galaxy collision scenarios and generate initial conditions for simulations.
