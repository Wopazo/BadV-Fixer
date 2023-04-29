# On importe les modules importants
import os
import shutil
import getpass
import configparser

# En-tête ASCII
print("""
██████╗  █████╗ ██████╗ ██╗   ██╗    ███████╗██╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔══██╗██║   ██║    ██╔════╝██║╚██╗██╔╝██╔════╝██╔══██╗
██████╔╝███████║██║  ██║██║   ██║    █████╗  ██║ ╚███╔╝ █████╗  ██████╔╝
██╔══██╗██╔══██║██║  ██║╚██╗ ██╔╝    ██╔══╝  ██║ ██╔██╗ ██╔══╝  ██╔══██╗
██████╔╝██║  ██║██████╔╝ ╚████╔╝     ██║     ██║██╔╝ ██╗███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═════╝   ╚═══╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                                                
""")

# Fonctions pour chaque option

# On définit la fonction libssl
def fonction_libssl():
    libs_dir = os.path.join(os.getcwd(), "libs")
# On récupère le chemin d'alt:v via interface utilisateur
    altv_dir = input("Entrez le chemin absolu du répertoire alt:v : ")
    altv_libs_dir = os.path.join(altv_dir, "libs")
# On met en place une erreur si le dossier libs est introuvable
    if not os.path.exists(altv_libs_dir):
        print("Le dossier libs n'existe pas dans le répertoire alt:v,vous avez surement sélectionné le mauvais dossier")
        exit()
    # On vérifie l'existence des fichiers
    libssl_path = os.path.join(altv_libs_dir, "libssl-1_1-x64.dll")
    libcrypto_path = os.path.join(altv_libs_dir, "libcrypto-1_1-x64.dll")
    if os.path.exists(libssl_path) and os.path.exists(libcrypto_path):
        print("Les dll sont déjà présent")
        return
    # On copie les fichiers dll si nécessaire
    for file_name in os.listdir(libs_dir):
        file_path = os.path.join(libs_dir, file_name)
        if os.path.isfile(file_path):
            shutil.copy(file_path, altv_libs_dir)
    print("Opération finie avec succès.")

def fonction_saltychat():
# Chemin absolu du dossier des plugins de TeamSpeak
    ts3_plugins_dir = os.path.join(os.getenv('APPDATA'), "TS3Client", "plugins")

# Chemin absolu du dossier SaltyChat dans le dossier plugins
    saltychat_dir = os.path.join(os.getcwd(), "plugins", "SaltyChat")

# Vérification si les fichiers/dossiers existent et suppression si nécessaire
    if os.path.exists(os.path.join(ts3_plugins_dir, "SaltyChat_win64.dll")):
        os.remove(os.path.join(ts3_plugins_dir, "SaltyChat_win64.dll"))
    if os.path.exists(os.path.join(ts3_plugins_dir, "SaltyChat_win32.dll")):
        os.remove(os.path.join(ts3_plugins_dir, "SaltyChat_win32.dll"))
    if os.path.exists(os.path.join(ts3_plugins_dir, "SaltyChat")):
        shutil.rmtree(os.path.join(ts3_plugins_dir, "SaltyChat"))

# Copie du dossier SaltyChat dans le dossier des plugins de TeamSpeak
    try:
        if os.path.exists(saltychat_dir):
            dst_dir = os.path.join(ts3_plugins_dir, "SaltyChat")
            if os.path.exists(dst_dir):
                shutil.rmtree(dst_dir)
            shutil.copytree(saltychat_dir, dst_dir)
            print("(1/2) Salty Chat a été installé!")
        else:
            print("Le dossier SaltyChat n'existe pas dans le dossier plugins !")
    except shutil.Error as e:
        print(f"Impossible de copier le dossier SaltyChat : {e}")
    except OSError as e:
        print(f"Impossible de copier le dossier SaltyChat : {e}")

    # Chemin absolu du dossier plugin dans le répertoire courant
    plugin_dir = os.path.join(os.getcwd(), "plugins")

    # Copie des fichiers de plugins vers le dossier des plugins de TeamSpeak
    try:
        for file_name in os.listdir(plugin_dir):
            file_path = os.path.join(plugin_dir, file_name)
            if os.path.isfile(file_path):
                shutil.copy(file_path, ts3_plugins_dir)
        print("(2/2) Salty Chat a été installé!")
    except shutil.Error as e:
        print(f"Impossible de copier les fichiers : {e}")
    except OSError as e:
        print(f"Impossible de copier les fichiers : {e}")

def fonction_settingsreset():
# On récupère le nom de l'utilisateur via le module "os"

    username = os.environ['USERNAME']
    path = f'C:\\Users\\{username}\\Documents\\Rockstar Games\\GTA V\\settings.xml'
# Si on trouve le fichier des settings gtaV, on le supprime (il sera remis automatiquement avec les paramètres défaut)
    if os.path.exists(path):
        os.remove(path)
        print(f"Les paramètres ont été réintiliasé")
    else:
        print(f"Impossible d'accéder aux paramètres")

def fonction_cachereset():
    user_folder = os.path.expanduser('~')
    cache_path = os.path.join(user_folder, 'AppData', 'Local', 'altv', 'cache')
# On supprime le fichier cache de altv
    shutil.rmtree(cache_path)
    print("Le cache a été supprimé avec succès.")

def fonction_timeout():
    username = os.getlogin()
    file_path = f'C:/Users/{username}/AppData/Local/altv/altv.toml'
# On vérifie si le fichier existe bien
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
# Si une fonction gérant le gameTimeout est présent, on ne touche à rien
                if 'gameTimeout' in line:
                    print("Erreur : La ligne gameTimeout existe déjà dans le fichier altv.toml.")
                    return
# Sinon, on ajoute cette fonction
        with open(file_path, 'a') as f:
            f.write("\ngameTimeout = 2000")
        print("Opération réussi avec succées")
    else:
        print("Erreur : Le fichier altv.toml n'existe pas.")
# On définit les options
options = [fonction_libssl, fonction_saltychat, fonction_settingsreset, fonction_cachereset, fonction_timeout]

while True:
    for i, option in enumerate(options):
        print(f"{i+1}. {option.__name__}")
        
    touche = input()
# On laisse la posibilité à l'utilisateur de quitter le logiciel
    if touche == "q":
        break
    if touche == "quit":
        break
    if touche == "exit":
        break
    elif touche.isdigit():
        choix = int(touche) - 1
        if choix < 0 or choix >= len(options):
            choix = 0
        options[choix]()  # Appel de la fonction correspondante à l'option choisie
    elif touche == "\x1b[A":  # Flèche haut
        choix -= 1
        if choix < 0:
            choix = len(options) - 1
    elif touche == "\x1b[B":  # Flèche bas
        choix += 1
        if choix >= len(options):
            choix = 0
