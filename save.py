def appendSave(dirType, dir):
    with open("asset/param/save.txt", "a") as f:
        f.write(f"{dirType}:{dir}\n")

def readSave(dirType):
    dir = None
    # Lire toutes les lignes du fichier
    with open("asset/param/save.txt", "r") as f:
        lines = f.readlines()

    # Filtrer les lignes, gardant tout sauf la ligne correspondant à dirType
    with open("asset/param/save.txt", "w") as f:
        for line in lines:
            if line.startswith(f"{dirType}:"):
                dir = line.split(":", 1)[1].strip()
            else:
                f.write(line)  # Réécrire les lignes non-correspondantes

    return dir
