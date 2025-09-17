import subprocess
import time
import webbrowser
#import requests
import winreg
import os

# Configuración del directorio de trabajo de git
git_dir = r"E:\1-UTEZ\4-Cuatrimestre\ProgramacionRedes\Trabajos2"

# Crea el directorio si no existe
if not os.path.exists(git_dir):
    os.makedirs(git_dir)
    print(f"Created directory: {git_dir}")

# Lista todos los repositorios en el directorio de trabajo
repos = [name for name in os.listdir(git_dir)
         if os.path.isdir(os.path.join(git_dir, name)) and
         os.path.exists(os.path.join(git_dir, name, ".git"))
]

# Imprime en pantalla los repositorios encontrados
if repos:
    print("Found the following GitHub repositories: ")
    for idx, repo in enumerate(repos, 1):
        print(f"{idx}, {repo}")
else:
    print("No hay repositorios seleccionados")
    print("Por favor, seleccione un repositorio valido")