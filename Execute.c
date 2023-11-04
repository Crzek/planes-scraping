#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>

int isPython(FILE *file)
{
    char version[128];                                 // str para almacenar la versión de Python
    if (fgets(version, sizeof(version), file) != NULL) // fgetd() lee la salida del comando
    {
        printf("Versión de Python instalada: %s", version);
        return 1;
    }
    else
    {
        printf("Python no está instalado en el sistema, Debes de Instalarlo\n");
        return 0;
    }
}

// funion que devuelve un string
// char getCurrentDIR()
// {
//     char cwd[1024];
//     if (getcwd(cwd, sizeof(cwd)) != NULL)
//     {
//         return cwd;
//     }
//     else
//     {
//         return "Error";
//     }
// }

int isVenv()
{
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) != NULL)
    {
        DIR *dir = opendir(strcat(cwd, "\\venv"));
        if (dir)
        {
            closedir(dir);
            return 1;
        }
        else
        {
            return 0;
        }
    }
    else
    {
        perror("Error al obtener el directorio actual");
        return 0;
    }
}

/// Ejecuta el archivo main.py
void executeMain()
{
    system("python main.py");
}

void executeVenv()

{
    system("venv\\Scripts\\activate.ps1");
}

int createVenv()
{
    system("python -m venv venv");
    return 0;
}

void installRequirements()
{
    system("pip install -r requirements.txt");
}

void installVenv()
{
    if (isVenv() == 1)
    {
        printf("Ejecutando Venv\n");
        executeVenv();
    }
    else
    {
        printf("No existe un entorno virtual, se creará uno.\n");
        createVenv();
        executeVenv();
        installRequirements();
    }
}

int main()
{
    // Ejecuta el comando 'python --version'
    FILE *cmd_output = popen("python --version", "r"); // popen() abrir proceso

    if (cmd_output == NULL)
    {
        printf("No se pudo ejecutar el comando.\n");
        return 1;
    }

    int py = isPython(cmd_output); // Verifica si Python está instalado

    if (py == 1)
    {
        installVenv();
        executeMain();
    }

    pclose(cmd_output);

    return 0;
}