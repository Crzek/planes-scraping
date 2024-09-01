#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>

int main()
{
    FILE *cmd_output = popen("dir", "r"); // popen() abrir proceso

    if (cmd_output == NULL)
    {
        printf("No se pudo ejecutar el comando.\n");
        return 1;
    }

    char buffer[128]; // Un búfer para almacenar los datos leídos

    while (fgets(buffer, sizeof(buffer), cmd_output) != NULL)
    {
        printf("%s", buffer); // Imprimir cada línea leída
    }

    pclose(cmd_output);

    return 0;
}