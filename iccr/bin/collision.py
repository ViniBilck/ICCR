import configparser
import argparse
from iccr import Collision


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Configuration File")
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config)
    galaxy1_properties = [config['Galaxy-1']['IC_PATH'],
                          [config['Galaxy-1.Position'].getfloat('X'),
                           config['Galaxy-1.Position'].getfloat('Y'),
                           config['Galaxy-1.Position'].getfloat('Z')],
                          [config['Galaxy-1.Velocity'].getfloat('X'),
                           config['Galaxy-1.Velocity'].getfloat('Y'),
                           config['Galaxy-1.Velocity'].getfloat('Z')],
                          [config['Galaxy-1.Rotation'].getfloat('X'),
                           config['Galaxy-1.Rotation'].getfloat('Y'),
                           config['Galaxy-1.Rotation'].getfloat('Z')]]
    galaxy2_properties = [config['Galaxy-2']['IC_PATH'],
                          [config['Galaxy-2.Position'].getfloat('X'),
                           config['Galaxy-2.Position'].getfloat('Y'),
                           config['Galaxy-2.Position'].getfloat('Z')],
                          [config['Galaxy-2.Velocity'].getfloat('X'),
                           config['Galaxy-2.Velocity'].getfloat('Y'),
                           config['Galaxy-2.Velocity'].getfloat('Z')],
                          [config['Galaxy-2.Rotation'].getfloat('X'),
                           config['Galaxy-2.Rotation'].getfloat('Y'),
                           config['Galaxy-2.Rotation'].getfloat('Z')]]
    _collision = Collision(galaxy1_properties[0], galaxy2_properties[0])
    _collision.do_rotation(0, 'XYZ', galaxy1_properties[3])
    _collision.do_rotation(1, 'XYZ', galaxy2_properties[3])
    _collision.initial_condition_file(pericenter=0, orbit=[galaxy1_properties[1],
                                                           galaxy2_properties[1],
                                                           galaxy1_properties[2],
                                                           galaxy2_properties[2]])
