import numpy as np
import tables
from scipy import integrate
from scipy.spatial.transform import Rotation

G_CONST_KPC = 44985


class Collision:
    def __init__(self, galaxyname1: str, galaxyname2: str):
        self.galaxyname1 = galaxyname1
        self.galaxyname2 = galaxyname2
        self.parttypes_in_hdf5 = "PartType0,PartType1,PartType2,PartType3,PartType4,PartType5".split(",")
        self.properties_in_hdf5 = "Coordinates,Velocities,ParticleIDs,Masses,InternalEnergy,Density,SmoothingLength," \
                                  "Potential,Acceleration".split(",")

    @staticmethod
    def initial_orbit(m1, m2, pericenter, escape_velocity=None):
        def v_esc(r_pericenter, g, m):
            ret = np.sqrt((2 * g * m) / r_pericenter)
            return ret

        def rtt_2(t, data, mass_1, mass_2, g):
            mg = (mass_1 + mass_2) * g
            x, y, z = data[:3]
            vx, vy, vz = data[3:6]
            ax = - mg * x / np.linalg.norm([x, y, z]) ** 3
            ay = - mg * y / np.linalg.norm([x, y, z]) ** 3
            az = - mg * z / np.linalg.norm([x, y, z]) ** 3
            return [vx, vy, vz, ax, ay, az]

        if escape_velocity is None:
            escape_velocity = v_esc(pericenter, G_CONST_KPC, m1 + m2)
        data_m1 = [0, pericenter, 0, escape_velocity, 0, 0]
        sol1 = integrate.solve_ivp(rtt_2, (0, 1),
                                   data_m1,
                                   args=(m1, m2, G_CONST_KPC),
                                   t_eval=np.arange(0, 1, 1e-4), method='Radau',
                                   rtol=1e-8,
                                   atol=1e-8)
        r = np.array([sol1.y[0], sol1.y[1], sol1.y[2]])
        r1 = (m2 / (m1 + m2)) * r
        r2 = -(m1 / (m1 + m2)) * r
        v = np.array([sol1.y[3], sol1.y[4], sol1.y[5]])
        v1 = (m2 / (m1 + m2)) * v
        v2 = -(m1 / (m1 + m2)) * v
        initial_coord_g1 = [r1[0][-1], r1[1][-1], r1[2][-1]]
        initial_coord_g2 = [r2[0][-1], r2[1][-1], r2[2][-1]]
        initial_veloc_g1 = [-1 * v1[0][-1], -1 * v1[1][-1], -1 * v1[2][-1]]
        initial_veloc_g2 = [-1 * v2[0][-1], -1 * v2[1][-1], -1 * v2[2][-1]]
        all_datas = {"Coord_G1": initial_coord_g1,
                     "Coord_G2": initial_coord_g2,
                     "Velocities_G1": initial_veloc_g1,
                     "Velocities_G2": initial_veloc_g2}
        return all_datas

    def get_mass(self):
        with tables.open_file(self.galaxyname1, "r") as galaxy1, tables.open_file(self.galaxyname2, "r") as galaxy2:
            galaxy1_mass_total = 0
            galaxy2_mass_total = 0
            for all_types in self.parttypes_in_hdf5:
                try:
                    galaxy1_mass = sum(getattr(galaxy1.root, f"{all_types}").Masses[:])
                    galaxy2_mass = sum(getattr(galaxy2.root, f"{all_types}").Masses[:])
                    galaxy1_mass_total = galaxy1_mass_total + galaxy1_mass
                    galaxy2_mass_total = galaxy2_mass_total + galaxy2_mass
                except ValueError:
                    print(f"There is no Masses in {all_types}")
        return [galaxy1_mass_total, galaxy2_mass_total]

    def get_particles(self):
        total_quantity = self.get_numparts()
        total = [sum(total_quantity[0:i]) for i in range(7)]
        return total

    def get_numparts(self):
        with tables.open_file(self.galaxyname1, "r") as galaxy1, tables.open_file(self.galaxyname2, "r") as galaxy2:
            total_part_1 = getattr(galaxy1.root.Header, "_v_attrs").NumPart_ThisFile[:]
            total_part_2 = getattr(galaxy2.root.Header, "_v_attrs").NumPart_ThisFile[:]
            total_quantity = total_part_1 + total_part_2
        return total_quantity

    def do_rotation(self, which_galaxy: int, rotation_sequence: str, angles: list):
        rotation_matrix = Rotation.from_euler(rotation_sequence, angles, degrees=True).as_matrix()
        if which_galaxy == 0:
            with tables.open_file(self.galaxyname1, "a") as galaxy1:
                for all_types in self.parttypes_in_hdf5:
                    try:
                        old_coords = getattr(galaxy1.root, f"{all_types}").Coordinates[:]
                        new_coords = np.matmul(old_coords, rotation_matrix)
                        old_veloci = getattr(galaxy1.root, f"{all_types}").Velocities[:]
                        new_veloci = np.matmul(old_veloci, rotation_matrix)
                        getattr(galaxy1.root, f"{all_types}").Coordinates[:] = new_coords
                        getattr(galaxy1.root, f"{all_types}").Velocities[:] = new_veloci
                    except ValueError:
                        print(f"There is no Coordinates or Velocities in {all_types}")
        if which_galaxy == 1:
            with tables.open_file(self.galaxyname2, "a") as galaxy2:
                for all_types in self.parttypes_in_hdf5:
                    try:
                        old_coords = getattr(galaxy2.root, f"{all_types}").Coordinates[:]
                        new_coords = np.matmul(old_coords, rotation_matrix)
                        old_veloci = getattr(galaxy2.root, f"{all_types}").Velocities[:]
                        new_veloci = np.matmul(old_veloci, rotation_matrix)
                        getattr(galaxy2.root, f"{all_types}").Coordinates[:] = new_coords
                        getattr(galaxy2.root, f"{all_types}").Velocities[:] = new_veloci
                    except ValueError:
                        print(f"There is no Coordinates or Velocities in {all_types}")

    def initial_condition_file(self, pericenter, escape_velocity=None, orbit=None):
        galaxies_masses = self.get_mass()
        if orbit is None:
            initial_orbits = self.initial_orbit(galaxies_masses[0], galaxies_masses[1], pericenter, escape_velocity)
        else:
            initial_orbits = {"Coord_G1": orbit[0],
                              "Coord_G2": orbit[1],
                              "Velocities_G1": orbit[2],
                              "Velocities_G2": orbit[3]}
        all_particleids = self.get_particles()
        numpart = self.get_numparts()
        print(f"ParticleIDs Array is {all_particleids}")
        with tables.open_file("collision_file.hdf5", "w") as collision_file:
            collision_file.create_group("/", "Header")
            getattr(collision_file.root.Header, "_v_attrs").NumPart_ThisFile = numpart
            getattr(collision_file.root.Header, "_v_attrs").NumPart_Total = numpart
            getattr(collision_file.root.Header, "_v_attrs").MassTable = np.array([0, 0, 0, 0, 0, 0])
            getattr(collision_file.root.Header, "_v_attrs").Time = 1.
            getattr(collision_file.root.Header, "_v_attrs").Redshift = 0.
            getattr(collision_file.root.Header, "_v_attrs").BoxSize = 35000.
            getattr(collision_file.root.Header, "_v_attrs").HubbleParam = 0.6774
            getattr(collision_file.root.Header, "_v_attrs").Omega0 = 0.3089
            getattr(collision_file.root.Header, "_v_attrs").OmegaBaryon = 0.0486
            getattr(collision_file.root.Header, "_v_attrs").OmegaLambda = 0.6911
            getattr(collision_file.root.Header, "_v_attrs").NumFilesPerSnapshot = 1
            with tables.open_file(self.galaxyname1, "r") as galaxy1, tables.open_file(self.galaxyname2, "r") as galaxy2:
                particle_count = 0
                for all_types in self.parttypes_in_hdf5:
                    collision_file.create_group("/", f"{all_types}")
                    for all_properties in self.properties_in_hdf5:
                        if all_properties == "Velocities":
                            galaxy1_vector = getattr(getattr(galaxy1.root, f"{all_types}"), f"{all_properties}")[:]
                            galaxy2_vector = getattr(getattr(galaxy2.root, f"{all_types}"), f"{all_properties}")[:]
                            galaxy1_vector_new = galaxy1_vector + initial_orbits["Velocities_G1"]
                            galaxy2_vector_new = galaxy2_vector + initial_orbits["Velocities_G2"]
                            properties_vector = np.append(galaxy1_vector_new, galaxy2_vector_new, axis=0)
                            collision_file.create_array(getattr(collision_file.root, f"{all_types}"),
                                                        f"{all_properties}", properties_vector)
                        elif all_properties == "Coordinates":
                            galaxy1_vector = getattr(getattr(galaxy1.root, f"{all_types}"), f"{all_properties}")[:]
                            galaxy2_vector = getattr(getattr(galaxy2.root, f"{all_types}"), f"{all_properties}")[:]
                            galaxy1_vector_new = galaxy1_vector + initial_orbits["Coord_G1"]
                            galaxy2_vector_new = galaxy2_vector + initial_orbits["Coord_G2"]
                            properties_vector = np.append(galaxy1_vector_new, galaxy2_vector_new, axis=0)
                            collision_file.create_array(getattr(collision_file.root, f"{all_types}"),
                                                        f"{all_properties}", properties_vector)
                        elif all_properties == "ParticleIDs":
                            newids = np.arange(all_particleids[particle_count], all_particleids[particle_count+1], 1)
                            collision_file.create_array(getattr(collision_file.root, f"{all_types}"),
                                                        f"{all_properties}", newids)
                            particle_count = particle_count + 1
                            print(particle_count) 
                        else:
                            galaxy1_vector = getattr(getattr(galaxy1.root, f"{all_types}"), f"{all_properties}")[:]
                            galaxy2_vector = getattr(getattr(galaxy2.root, f"{all_types}"), f"{all_properties}")[:]
                            properties_vector = np.append(galaxy1_vector, galaxy2_vector, axis=0)
                            collision_file.create_array(getattr(collision_file.root, f"{all_types}"),
                                                        f"{all_properties}", properties_vector)
