import mitsuba as mi

mi.set_variant('scalar_rgb')

img = mi.render(mi.load_file('test00001.xml'))

mi.Bitmap(img).write('mitsuba.exr')