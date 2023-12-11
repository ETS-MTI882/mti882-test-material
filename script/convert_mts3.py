import json
import argparse
import math 

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()

def export_integrator(out):
    # Create integrator path
    out.write('    <integrator type="path">\n')
    out.write('        <integer name="max_depth" value="5"/>\n')
    out.write('        <boolean name="hide_emitters" value="false"/>\n')
    out.write('    </integrator>\n')

def export_transformation(out, t):
    if type(t) == list:
        for tt in t:
            export_transformation(out, tt) 
        return
    
    if args.debug:
        print(f"[DEBUG] Transformation: {t}")
    
    if "from" in t and "at" in t and "up" in t:
        out.write(f'''<lookat target="{t["at"][0]}, {t["at"][1]}, {t["at"][2]}" 
                    origin="{t["from"][0]}, {t["from"][1]}, {t["from"][2]}" 
                    up="{t["up"][0]}, {t["up"][1]}, {t["up"][2]}"/>\n''')
    elif "matrix" in t:
        transform = t["matrix"]
        out.write(f'''<matrix value="{transform[0]}, {transform[1]}, {transform[2]}, {transform[3]}, {transform[4]}, {transform[5]}, {transform[6]}, {transform[7]}, {transform[8]}, {transform[9]}, {transform[10]}, {transform[11]}, {transform[12]}, {transform[13]}, {transform[14]}, {transform[15]}"/>\n''')
    elif "translate" in t:
        transform = t["translate"]
        out.write(f'''<translate x="{transform[0]}" y="{transform[1]}" z="{transform[2]}"/>\n''')
    elif "scale" in t:
        transform = t["scale"]
        if type(transform) == list:
            out.write(f'''<scale value="{transform[0]}, {transform[1]}, {transform[2]}"/>\n''')
        else:
            out.write(f'''<scale value="{transform}"/>\n''')
    elif "axis" in t and "angle" in t:
        out.write(f'''<rotate value="{t["axis"][0]},{t["axis"][1]},{t["axis"][2]}" angle="{t["angle"]}"/>\n''')
    elif "rotation" in t:
        out.write(f'''<rotate value="0, 0, 1" angle="{t["rotation"][2]}" />\n''')
        out.write(f'''<rotate value="1, 0, 0" angle="{t["rotation"][0]}" />\n''')
        out.write(f'''<rotate value="0, 1, 0" angle="{t["rotation"][1]}" />\n''')
    elif "x" in t or "y" in t or "z" in t or "o" in t:
        x = t["x"] if "x" in t else [1.0, 0.0, 0.0]
        y = t["y"] if "y" in t else [0.0, 1.0, 0.0]
        z = t["z"] if "z" in t else [0.0, 0.0, 1.0]
        o = t["o"] if "o" in t else [0.0, 0.0, 0.0]
        out.write(f'''<matrix value="{x[0]}, {y[0]}, {z[0]}, {o[0]}, {x[1]}, {y[1]}, {z[1]}, {o[1]}, {x[2]}, {y[2]}, {z[2]}, {o[2]}, 0.0, 0.0, 0.0, 1.0"/>\n''')
    else:
        print(f"[WARN] Unsupported transformation type: {t}")
        out.write('<matrix value="1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1 ,0, 0, 0, 0, 1"/>\n')

def export_to_world(out, data):
    if "transform" in data:
        out.write('<transform name="to_world">\n')
        export_transformation(out, data["transform"])
        out.write('</transform>\n')

def export_sensor(out, data):
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
    # Change vertical fov to horizontal fov
    fov = data['camera']['vfov']
    aspect_ratio = data['camera']['resolution'][0] / data['camera']['resolution'][1]
    hfov = 2 * math.atan(math.tan(fov / 2) * aspect_ratio)
    
    # -- FOV
    out.write(f'''
            <string name="fov_axis" value="y" />
            <float name="fov" value="{data['camera']['vfov']}" />
            <float name="aperture_radius" value="0.0" />
            <sampler type="independent">
                <integer name="sample_count" value="64" />
            </sampler>''')

    export_to_world(out, data['camera'])
    
    out.write('    </sensor>\n') # End sensor

def parse_values(entry):
    if args.debug:
        print(f"[DEBUG] Value: {entry}")
    if type(entry) == list:
        return [entry[0], entry[1], entry[2]]
    if type(entry) == dict:
        # Check if it is constant
        if entry['type'] == 'constant':
            return entry['value']
        else:
            # Not supported
            print(f"[WARN] Unsupported value type: {entry['type']}")
            return [0.5, 0.5, 0.5]
    else:
        return [entry, entry, entry]    

def export_bsdf(out, bsdf):
    if args.debug:
        print(f"[DEBUG] bsdf: {bsdf}")
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
        print(f'[WARN] Unsupported material type: {bsdf}')
        # Export default material
        out.write(f'''
        <bsdf type="diffuse" id="{bsdf["name"]}">
        <rgb name="reflectance" value="0.5, 0.5, 0.5"/>
        </bsdf>\n''')

def export_shape(out, shape):
     # --- Export shape
    if shape['type'] == 'mesh':
        out.write(f'''<shape type="obj">
        <string name="filename" value="{shape['filename']}" />
        <ref id="{shape["material"]}" />\n''')
        export_to_world(out, shape)
        out.write(f'''</shape>\n''')
    elif shape['type'] == 'sphere':
        out.write(f'''<shape type="sphere">
        <float name="radius" value="{shape['radius']}" />
        <ref id="{shape["material"]}" />\n''')
        export_to_world(out, shape)
        out.write(f'''</shape>\n''')
    elif shape['type'] == 'quad':
        out.write(f'''<shape type="rectangle">
                  <transform name="to_world">''')
        # Transform
        # -- Export scale if necessary
        if 'size' in shape:
            size = shape['size']
            if args.debug:
                print(f"[DEBUG] Size: {size}") 
            if type(size) == list:
                out.write(f'''<scale x="{size[0] / 2.0}"  y="{size[1] / 2.0}" z="1.0" />''')
            else: 
                out.write(f'''<scale value="{size / 2.0}" />''')
        export_transformation(out, shape['transform'])  
        out.write("</transform>\n")
        
        out.write(f'''<ref id="{shape["material"]}" />\n''')
        out.write(f'''</shape>\n''')
    else:
        print(f'[WARN] Unsupported shape type: {shape}')

with open(args.input, 'r') as f:
    data = json.load(f)

out = open(args.output, 'w')
out.write('<scene version="2.0.0">\n')

export_integrator(out)
export_sensor(out, data)

# --- Export materials
for bsdf in data['materials']:
    export_bsdf(out, bsdf)

# --- Export shapes
for shape in data['shapes']:
   export_shape(out, shape)

out.write('</scene>\n')
    