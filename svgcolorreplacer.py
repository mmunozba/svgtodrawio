from os import listdir, mkdir, path
from sys import argv

# Adds CSS color fill to svg
def search_and_replace(svg_string, color):
    # Find first > after <svg
    first_close_bracket_position = svg_string.find(">")
    # Add style css style
    css_style = '<style type="text/css">.iconincolor{fill:' + color + ';}</style>'

    new_svg_string = svg_string[:first_close_bracket_position+1] + css_style + svg_string[first_close_bracket_position+1:]
    # Find <path
    path_position = new_svg_string.find("<path")
    class_string = f' class="iconincolor"'
    final_svg_string = new_svg_string[:path_position+5] + class_string + new_svg_string[path_position+5:]
    return final_svg_string

if __name__ == "__main__":
    # Check if input arguments are present
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

    output_file_path = f"{input_file_path}{color}/"
    if not path.exists(output_file_path):
        mkdir(output_file_path)

    # Loop over all files in input folder
    for input_filename in listdir(input_file_path):
        if input_filename.endswith(".svg"):
            #   Read file to string
            with open(f"{input_file_path}{input_filename}", "r") as svg_file:
                svg_string = svg_file.read()
            #   Replace color in string
            new_svg_string = search_and_replace(svg_string, color)
            #   Save string to new file
            with open(f"{output_file_path}{input_filename}", "w") as new_svg_file:
                new_svg_file.write(new_svg_string)
