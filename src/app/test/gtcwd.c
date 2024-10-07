#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>

int main(int argc, char const *argv[])
{
    char currentDirectory[FILENAME_MAX]; // Declarar un arreglo para almacenar el directorio actual

    if (getcwd(currentDirectory, sizeof(currentDirectory)) != NULL)
    {

        DIR *dir = opendir(strcat(currentDirectory, "\\venv"));
        if (dir)
        {
            closedir(dir);
            printf("La carpeta existe.\n");
        }
        else
        {
            printf("La carpeta no existe o no se puede acceder.\n");
        }
        printf("Directorio actual: %s\n", currentDirectory);
    }
    else
    {
        perror("Error al obtener el directorio actual");
    }

    return 0;
    return 0;
}
