from PIL import Image, ImageOps
from math import ceil, floor
from requests import get
import easygui
import os;

# Only png files are supported
files = easygui.fileopenbox('Sprites', 'Seleccionar imagenes', '*.png', multiple=True)
output = easygui.diropenbox('Seleccionar carpeta de salida', 'Seleccionar carpeta de salida', '.');

# If doesn't files selected exit
if files == None:
    print("[ERROR] No files selected!");
    exit()

if output == None:
    print('[ERROR] No output folder selected')
    exit()

def proccess_sprite(path, output):
    # Prompt user for the number of rows and columns by default is 4
    rowPromps = int(easygui.multenterbox('Input rows', 'Number of rows', ['rows'], ['4'])[0])
    
    # Vars
    rows = rowPromps
    square = floor(1024 / rows);
    filename = os.path.basename(path)

    print(f'[INFO] Rows: {rows}')

    # if filename includes _merged, remove from filename
    if '_merged' in filename:
        filename = filename.replace('_merged', '')
    
    spritesheet = Image.open(path)
    main_sprite = spritesheet.crop((0, 0, spritesheet.size[0], 750));
    faces_sprites = spritesheet.crop((0, 770, spritesheet.size[0], spritesheet.size[1]));


    # Get Info from the spritesheet in atlas
    print("[INFO] Getting info from atlas academy...");

    req = get(f'https://api.atlasacademy.io/raw/JP/svtScript?charaId={filename[:-4]}&lang=en');
    res = req.json();

    faceX = res[0]['faceX'];
    faceY = res[0]['faceY'];

    print(f'[INFO] Got info from atlas academy:');
    print(f'[INFO] faceX: {faceX}');
    print(f'[INFO] faceY: {faceY}');

    # Make directory for faces
    if not os.path.exists(f'{output}/{filename[:-4]}/faces'):
        print("[INFO] Creating directory for faces...");
        os.makedirs(f'{output}/{filename[:-4]}/faces');
        
    if not os.path.exists(f'{output}/{filename[:-4]}/body'):
        print("[INFO] Creating directory for body...");
        os.makedirs(f'{output}/{filename[:-4]}/body');# Make directory for body

    # Generate Sprites
    print("[INFO] Generating sprites...");
    for y in range(0, ceil(faces_sprites.size[1] / square)):
        imgContainer = faces_sprites.crop((0, (square * y) - 2,  faces_sprites.size[0], square * (y + 1)))

        for x in range(0, ceil(imgContainer.size[0] / square)):
            # Face
            faceContainer = imgContainer.crop((0, square * 0,  faces_sprites.size[0], square * 1))
            face = faceContainer.crop((faceContainer.size[0] - square * (x + 1), 0, faceContainer.size[0] - square * x, faceContainer.size[1]))
            
            # Paste face on main sprite
            main_sprite.paste(face, (faceX, faceY))
            
            # Save Face And Body
            face.save(f'{output}/{filename[:-4]}/faces/face_{y}_{x}.png')
            ImageOps.contain(main_sprite, (1920, 1080)).save(f'{output}/{filename[:-4]}/body/body_{y}_{x}.png')

    print("[INFO] Done!");
    
    
# Process all sprites
for file in files:
    print(f'[INFO] Processing {file}...');
    proccess_sprite(file, output)
    print('\n')
