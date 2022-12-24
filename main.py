import os
import tempfile
import sys
from PIL import Image
import tinify
import shutil  # Ajout de l'import de shutil

TINIFY_API_KEY = "MrRNg7WbrybQ5kVRwqtHVpxb2ZQyVWGR"

MAX_SIZE = (1024, 1024)


def resize_image(image_path):
    with Image.open(image_path) as image:
        # Redimensionnez l'image en conservant les proportions originales
        image.thumbnail(MAX_SIZE, Image.ANTIALIAS)

        # Créez un fichier temporaire pour enregistrer l'image modifiée
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
            # Séparez le nom du fichier et l'extension à partir du chemin du fichier d'origine
            _, extension = os.path.splitext(image_path)
            # Enlevez le point et mettez l'extension en majuscule
            extension = extension[1:].upper()

            # Vérifiez si l'extension est prise en charge par la bibliothèque PIL
            if extension in Image.SAVE:
                image.save(temp_file_path, extension)
            else:
                print(
                    f"L'extension '{extension}' n'est pas prise en charge par la bibliothèque PIL. L'image sera enregistrée en format JPEG par défaut.")
                image.save(temp_file_path, "JPEG")

        return temp_file_path


def optimize_image(image_path):
    tinify.key = TINIFY_API_KEY
    source = tinify.from_file(image_path)
    source.to_file(image_path)


def process(file_path, dest_dir):
    print("Traitement de l'image: ", file_path)
    # Vérifiez le type de fichier de l'image
    # Redimensionnez l'image si c'est un fichier image valide
    resized_file_path = resize_image(file_path)

    # Optimisez l'image redimensionnée
    optimize_image(resized_file_path)

    # Enregistrez l'image modifiée dans le répertoire de destination
    shutil.copy(resized_file_path, os.path.join(
        dest_dir, os.path.basename(file_path)))


def main():
    print("Début du traitement des images")
    # Récupérez les arguments de la ligne de commande
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    print(input_dir, output_dir)

    # Vérifiez que les répertoires d'entrée et de sortie existent
    if not os.path.exists(input_dir):
        print("Le répertoire d'entrée n'existe pas")
        sys.exit(1)

    if not os.path.exists(output_dir):
        print("Le répertoire de sortie n'existe pas")
        sys.exit(1)

    # Appelez la fonction process sur chaque fichier dans le répertoire source
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        process(file_path, output_dir)


if __name__ == "__main__":
    main()
