import numpy as np
import tables
from scipy import integrate

G_CONST_KPC = 44985


class Collision:
    def __init__(self):
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
        initial_veloc_g1 = [v1[0][-1], v1[1][-1], v1[2][-1]]
        initial_veloc_g2 = [v2[0][-1], v2[1][-1], v2[2][-1]]
        all_datas = {"Coord_G1": initial_coord_g1,
                     "Coord_G2": initial_coord_g2,
                     "Velocities_G1": initial_veloc_g1,
                     "Velocities_G2": initial_veloc_g2}
        return all_datas

    def initial_condition_file(self, galaxyfile1, galaxyfile2):
        with tables.open_file(galaxyfile1, "r") as galaxy1, tables.open_file(galaxyfile2, "r") as galaxy2:
            for all_types in self.parttypes_in_hdf5:
                for all_properties in self.properties_in_hdf5:
                    print("Gal1", getattr(getattr(galaxy1.root, f"{all_types}"), f"{all_properties}"))
                    print("Gal2", getattr(getattr(galaxy2.root, f"{all_types}"), f"{all_properties}"))
