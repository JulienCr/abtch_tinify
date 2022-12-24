import os
import sys
import tinify
import shutil  # Ajout de l'import de shutil
import cv2


TINIFY_API_KEY = "MrRNg7WbrybQ5kVRwqtHVpxb2ZQyVWGR"

MAX_SIZE = (800, 800)


def resize_image(image_path):
    # Charger l'image en mémoire
    image = cv2.imread(image_path)

    height, width = image.shape[:2]
    if height > width:
        ratio = height / MAX_SIZE[0]
        image = cv2.resize(image, (int(width / ratio), MAX_SIZE[0]))
    else:
        ratio = width / MAX_SIZE[1]
        image = cv2.resize(image, (MAX_SIZE[1], int(height / ratio)))

    if not os.path.exists('temp'):
        os.makedirs('temp')

    image_path = os.path.join('temp', os.path.basename(image_path))
    cv2.imwrite(image_path, image)

    return image_path


def optimize_image(image_path):
    tinify.key = TINIFY_API_KEY
    source = tinify.from_file(image_path)
    source.to_file(image_path)


def process(file_path, dest_dir):

    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() not in (".jpg", ".png", ".jpeg"):
        print("Le fichier {} n'est pas une image valide. Il sera ignoré.".format(
            file_path))
        return

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
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "input"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"

    print(input_dir, output_dir)

    # Créez les répertoires d'entrée et de sortie s'ils n'existent pas
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Appelez la fonction process sur chaque fichier dans le répertoire source
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        process(file_path, output_dir)

    # Delete temp directory
    shutil.rmtree('temp')
    print("Fin du traitement des images")


if __name__ == "__main__":
    main()
