const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const Tinify = require('tinify');
const { execSync } = require('child_process');
const os = require('os');

const TINIFY_API_KEY = "MrRNg7WbrybQ5kVRwqtHVpxb2ZQyVWGR";
const MAX_SIZE = [800, 800];

async function resizeImage(imagePath) {
    const tempPath = path.join('temp', path.basename(imagePath));
    if (!fs.existsSync('temp')) {
        fs.mkdirSync('temp');
    }

    await sharp(imagePath)
        .resize({ width: MAX_SIZE[0], height: MAX_SIZE[1], fit: 'inside' })
        .toFile(tempPath);

    return tempPath;
}

async function optimizeImage(imagePath) {
    Tinify.key = TINIFY_API_KEY;
    await Tinify.fromFile(imagePath).toFile(imagePath);
}

async function process(filePath, destDir) {
    const fileExtension = path.extname(filePath).toLowerCase();
    if (![".jpg", ".png", ".jpeg"].includes(fileExtension)) {
        console.log(`Le fichier ${filePath} n'est pas une image valide. Il sera ignoré.`);
        return;
    }

    console.log("Traitement de l'image: ", filePath);
    const resizedFilePath = await resizeImage(filePath);
    await optimizeImage(resizedFilePath);

    const command = os.platform() === 'win32' ? `copy ${resizedFilePath} ${path.join(destDir, path.basename(filePath))}` : `cp ${resizedFilePath} ${path.join(destDir, path.basename(filePath))}`;
    execSync(command);
}

async function main() {

    console.log("Début du traitement des images");
    const inputDir = "input";
    const outputDir = "output";

    if (!fs.existsSync(inputDir)) {
        fs.mkdirSync(inputDir);
    }

    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
    }

    const files = fs.readdirSync(inputDir);
    for (const file of files) {
        const filePath = path.join(inputDir, file);
        await process(filePath, outputDir);
    }

    execSync('rm -rf temp');
    console.log("Fin du traitement des images");
}

main().catch(err => console.error(err));
