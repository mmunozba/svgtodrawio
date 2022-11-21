from sys import argv
from os import listdir, mkdir, path
from svgcolorreplacer import search_and_replace
from base64 import b64encode
from uuid import uuid4

# Takes an svg string of an image and returns the draw.io compatible XML string
def generate_xml_string(svg_string, title):
    imagedata = b64encode(svg_string.encode('ascii')).decode('ascii')

    # Extract image dimensions from svg
    viewbox_start = svg_string.find('viewBox="')
    svg_string_after_viewbox = svg_string[viewbox_start+9:]
    viewbox_string = svg_string_after_viewbox[:svg_string_after_viewbox.find('"')]

    minx, miny, w, h = viewbox_string.split(' ')
    aspect = "fixed"
    return f'{{"data":"data:image/svg+xml;base64,{imagedata};editableCssRules=.*;","w":{w},"h":{h},"title":"{title}","aspect":"{aspect}"}},'

if __name__ == "__main__":
    # Check if input arguments are present
    print("Checking input arguments...")
    try:
        input_file_path = argv[1]
        if input_file_path.startswith('#'):
            print("Only color provided as input.")
            argv[2] = input_file_path
            raise IndexError 
    except IndexError:
        input_file_path = input("Enter the folder path with the svg files: ")        
    try:
        color = argv[2]
    except IndexError:
        color = input("Enter the color you want for the svg files: ")

    # Loop over all files in input folder
    xml_library_string = '<mxlibrary>['
    input_folder_name = input_file_path.split('/')[-2]
    xml_library_file_name = f'{input_folder_name}.xml'
    print("Converting svg files...")
    for input_filename in listdir(input_file_path):
        if input_filename.endswith(".svg"):
            #   Read file to string
            with open(f"{input_file_path}{input_filename}", "r") as svg_file:
                svg_string = svg_file.read()
            #   Replace color in string
            new_svg_string = search_and_replace(svg_string, color)
            title = path.splitext(input_filename)[0]
            xml_string = generate_xml_string(new_svg_string, title)
            xml_library_string = xml_library_string + xml_string
    
    xml_library_string = xml_library_string[:-1] + ']</mxlibrary>'
    with open(f"{xml_library_file_name}", "w") as xml_library_file:
        xml_library_file.write(xml_library_string)
    print(f'Conversion successful. Library saved as "{xml_library_file_name}".')
