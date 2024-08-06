import sys
import yaml
import numpy as np

kinds = ['new', 'old']
scales = ['mi', 'sol']

class Flute:
    def __init__(self, name, kind):
        """
        :param name: scale
        :param kind: new / old
        """
        self.config = yaml.safe_load(open('./{0}.yml'.format(name)))
        self.kind = kind
        self.back_ratios = []
        self.front_ratios = []
        self.hole_ratio = None
        self.back_hole_location = None
        # print("Gathering stats of {0} flute on {1} scale".format(kind, self.config['name']))
        self.get_ratios_length()
        self.get_ratios_hole_and_diameter()

    def get_ratios_length(self):
        length = self.config['raw_data'][self.kind]['length']
        # back:
        back_structure = self.config['raw_data'][self.kind]['back_structure']
        agg_back_structure = [sum(back_structure[0:i+1]) for i in range(len(back_structure))]
        self.back_ratios = [l / length for l in agg_back_structure]

        # print('Back proportions:', "{0}".format(", ".join(["{0:.3f}%".format(l * 100) for l in back_ratios])))
        # print("Back hole location: {0:.3f}% from top.".format(sum(self.back_ratios[:2])/2 * 100))
        self.back_hole_location = sum(self.back_ratios[:2])/2
        # print(self.back_hole_location)
        agg_front_structure = self.config['agg_data'][self.kind]['face_structure']
        self.front_ratios = [l / length for l in agg_front_structure]
        # print('Front proportions:', "{0} from top.".format(", ".join(["{0:.3f}%".format(l * 100) for l in self.front_ratios])))

    def get_ratios_hole_and_diameter(self):
        width = self.config['raw_data'][self.kind]['width']
        a_hole = self.config['raw_data'][self.kind]['a_hole']
        self.hole_ratio = a_hole / width
        # print("Proportions between hole/width: {0:.3f}%".format(self.hole_ratio))
        # print()


def get_all_flutes():
    floots = []
    for scale in scales:
        for kind in kinds:
            floots.append(Flute(scale, kind))
    return floots


def get_flutes_of_scale(scale):
    if scale not in scales:
        print('Error, no such scale in DB. exiting')
        sys.exit()
    floots = []
    for kind in kinds:
        floots.append(Flute(scale, kind))
    return floots


def set_me_a_flute(length, diameter, scale=None):
    if scale:
        floots = get_flutes_of_scale(scale)
    else:
        floots = get_all_flutes()
    print('Setting up a flute with length {0} and width {1}'.format(length, diameter))
    back_hole_location = np.average([floot.back_hole_location for floot in floots])
    print("Back hole location: {0:.3f} cm from top.".format(back_hole_location * length))
    hole_ratio = np.average([floot.hole_ratio for floot in floots])
    print('Hole diameter: {0:.3f} cm.'.format(hole_ratio * diameter))
    front_ratios_array = np.array([f.front_ratios for f in floots])
    front_ratios_avg = np.average(front_ratios_array, axis=0)
    print('Front holes locations:', "{0} cm from top.".format(", ".join(["{0:.3f}".format(l * length) for l in front_ratios_avg])))
    print()


def main():
    length = 51
    diameter = 1.8
    set_me_a_flute(length, diameter)
    set_me_a_flute(length, diameter, scale='mi')
    set_me_a_flute(length, diameter, scale='sol')


if __name__ == '__main__':
    main()
