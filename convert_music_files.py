import os
import sys
import subprocess


def convert_input_to_output(input_format, output_format, input_folder, output_folder):
    # Überprüfe, ob der Ausgabeordner existiert, andernfalls erstelle ihn
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Durchlaufe den Eingabeordner
    for file_name in os.listdir(input_folder):
        print("FILE: " + file_name)
        
        if file_name.endswith("." + str(input_format)):

            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + "." + str(output_format))

            print("Check existence of " + output_file_path)
            if os.path.isfile(output_file_path):
                print(file_name + " exists. continue...")
                continue
            else:
                print("File not found. Start converting...")
            
            # Verwende ffmpeg, um die M4A-Datei in MP3 umzuwandeln
            subprocess.run(["ffmpeg", "-i", input_file_path, "-codec:a", "libmp3lame", "-q:a", "2", output_file_path], capture_output=True)
            print(output_file_path + " converted successfully!")
        print("")

    print("Umwandlung abgeschlossen.")

if __name__ == "__main__":
    # Überprüfe, ob der korrekte Befehl verwendet wurde
    if len(sys.argv) != 4:
        print("Verwendung: python convert.py <input_directory> <input_format> <output_format>")
        sys.exit(1)

    input_folder = sys.argv[1]
    input_format = sys.argv[2]
    output_format = sys.argv[3]
    output_folder = input_folder.replace(input_format, output_format, 1)

    # Führe die Umwandlung durch
    convert_input_to_output(input_format, output_format, input_folder, output_folder)

