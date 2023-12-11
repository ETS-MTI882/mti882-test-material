import mitsuba as mi
import argparse

# Parse arguments:
parser = argparse.ArgumentParser()
parser.add_argument('--scene', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
args = parser.parse_args()

mi.set_variant('scalar_rgb')

img = mi.render(mi.load_file(args.scene))

mi.util.write_bitmap(args.output, img)