#!/bin/bash
#como usar el siguiente script
#una vez tengas este archivo en tu terminal ejecuta el siguiente comando:
#  "chmod +x install_libraries.sh"
#una vez ejecutado el comando anterior ejecuta el siguiente comando:
#   "sudo ./install_libraries.sh"  
# "ATENCION: EJECUTAR LOS COMANDOS SIN COMILLAS.."


#*Función para instalar pip si no está instalado
function instalar_pip() {
    if ! command -v pip &> /dev/null; then
        echo "Instalando pip..."
        #*Instalamos pip utilizando el sistema de gestión de paquetes específico de la distribución
        sudo apt-get update
        sudo apt-get install -y python3-pip
    else
        echo "pip ya está instalado."
    fi
}

#*Lista de bibliotecas de Python a instalar
#*Agrega o quita bibliotecas según tus necesidades
LIBS=("speech_recognition" "pyttsx3" "pywhatkit" "pyaudio" "gtts" "playsound" "requests")

#*Comprobar si pip está instalado
instalar_pip

#*Instalar las bibliotecas
for lib in "${LIBS[@]}"; do
    echo "Instalando $lib..."
    pip install "$lib"
done

echo "Todas las bibliotecas han sido instaladas con éxito."
