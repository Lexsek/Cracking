#include <time.h>
#include <stdio.h>

int main(int argc, char ** argv){

    if(argc != 2){
        puts("Usage: ./decrypt <seed>");
        return 1;
    }

    srandom(atoi(argv[1]));

    char encByte;
    int randNumber;
    FILE *flag = NULL;
    FILE *out = fopen("out.txt", "r");

    if (out == NULL){
        puts("Couldn't open out.txt");
        return 1;
    }
    
    for (flag = fopen("flag.txt", "w"); ; fputc((randNumber % 1638 + 1) ^ encByte, flag)){
        encByte = getc(out);
        if (encByte == -1){
            break;
        }
        randNumber = random();
    }

    fclose(flag);
    fclose(out);

    flag = NULL;
    out = NULL;

    return 0;
}
