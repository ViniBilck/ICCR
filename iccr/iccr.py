import numpy as np
import tables


class Collision:
    def __init__(self):
        self.partsHDF5 = "PartType0,PartType1,PartType2,PartType3,PartType4,PartType5".split(",")

    @staticmethod
    def initialcondition(namecollision, galaxyfile1, galaxyfile2):
        with tables.open_file(namecollision, "w") as collision_file:
            with tables.open_file(galaxyfile1, "r") as galaxy1, tables.open_file(galaxyfile2, "r") as galaxy2:
                print(galaxy1.root)
                print(galaxy2.root)
        collision_file.create_group("/", "Header")
