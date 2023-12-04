import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
args = parser.parse_args()

with open(args.input, 'r') as f:
    data = json.load(f)

out = open(args.output, 'w')
out.write('<scene version="2.0.0">\n')

# Create integrator path
out.write('    <integrator type="path">\n')
out.write('        <integer name="max_depth" value="5"/>\n')
out.write('        <boolean name="hide_emitters" value="false"/>\n')
out.write('    </integrator>\n')

# Create sensor
out.write('    <sensor type="thinlens">\n')
# -- Resolution
out.write(f'''
          <film type="hdrfilm">
			<integer name="width" value="{data['camera']['resolution'][0]}" />
			<integer name="height" value="{data['camera']['resolution'][1]}" />
			<string name="file_format" value="openexr" />
			<rfilter type="box" />
		</film>\n''')
# -- FOV
out.write(f'''
        <float name="fov" value="{data['camera']['vfov']}" />
		<float name="aperture_radius" value="0.0" />
		<sampler type="independent">
			<integer name="sample_count" value="64" />
		</sampler>''')
# -- Transform
camera_from = data['camera']['transform']["from"]
camera_at = data['camera']['transform']["at"]
camera_up = data['camera']['transform']["up"]
out.write(f'''
        <transform name="to_world">
            <lookat target="{camera_at[0]}, {camera_at[1]}, {camera_at[2]}" 
                    origin="{camera_from[0]}, {camera_from[1]}, {camera_from[2]}" 
                    up="{camera_up[0]}, {camera_up[1]}, {camera_up[2]}"/>
        </transform>\n''')
out.write('    </sensor>\n') # End sensor

def parse_values(entry):
    print(entry)
    if type(entry) == list:
        return [entry[0], entry[1], entry[2]]
    if type(entry) == dict:
        # Check if it is constant
        if entry['type'] == 'constant':
            return entry['value']
        else:
            # Not supported
            print(f"Unsupported value type: {entry['type']}")
            return [0.5, 0.5, 0.5]            

# --- Export materials
for bsdf in data['materials']:
    print(bsdf)
    # Assuming no textures
    if bsdf['type'] == 'diffuse':
        albedo = parse_values(bsdf['albedo'])
        out.write(f'''
        <bsdf type="diffuse" id="{bsdf["name"]}">
        <rgb name="reflectance" value="{albedo[0]}, {albedo[1]}, {albedo[2]}"/>
        </bsdf>\n''')
    elif bsdf['type'] == 'diffuse_light':
        radiance = parse_values(bsdf['radiance'])
        out.write(f'''
        <emitter type="area" id="{bsdf["name"]}">
            <rgb name="radiance" value="{radiance[0]}, {radiance[1]}, {radiance[2]}"/>
        </emitter>\n''')
    else:
        print(f'Unsupported material type: {bsdf["type"]}')
        # Export default material
        out.write(f'''
        <bsdf type="diffuse" id="{bsdf["name"]}">
        <rgb name="reflectance" value="0.5, 0.5, 0.5"/>
        </bsdf>\n''')

# --- Export shapes
for shape in data['shapes']:
    # Assume array of 16 floats for the transform
    transform = shape['transform']["matrix"]
    # --- Export shape
    if shape['type'] == 'mesh':
        out.write(f'''
    <shape type="obj">
        <string name="filename" value="{shape['filename']}" />
        <ref id="{shape["material"]}" />
        <transform name="to_world">
            <matrix value="{transform[0]}, {transform[1]}, {transform[2]}, {transform[3]},
                    {transform[4]}, {transform[5]}, {transform[6]}, {transform[7]},
                    {transform[8]}, {transform[9]}, {transform[10]}, {transform[11]},
                    {transform[12]}, {transform[13]}, {transform[14]}, {transform[15]}"/>
        </transform>
    </shape>\n''')

out.write('</scene>\n')
    