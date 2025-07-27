#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include "common.h"

extern void feedOblivInt(obliv int *dest, int party, int value);
extern void revealOblivInt(int *dest, obliv int *src, int party);

#define PORT 54321

int main()
{
    printf("Guess the number: ");
    fflush(stdout);

    int input;
    if (scanf("%d", &input) != 1)
    {
        printf("Invalid input\n");
        return 1;
    }

    ProtocolDesc pd;
    int retry = 5;
    while (protocolAcceptTcp2P(&pd, "localhost") != 0 && retry-- > 0)
    {
        sleep(1);
    }
    if (retry < 0)
    {
        return 1;
    }

    fprintf(stderr, "[P1] Accepted connection from Party 2\n");
    setCurrentParty(&pd, 1);

    ProtocolIO io;
    memset(&io, 0, sizeof(io));
    feedOblivInt(&io.guess, 1, input);
    feedOblivInt(&io.secret, 2, 0); // dummy

    execYaoProtocol(&pd, compare, &io);

    int result = 0;
    revealOblivInt(&result, &io.match, 1);
    printf("Result: %d\n", result);

    if (result)
    {
        FILE *fp = fopen("flag.txt", "r");

        char flag[128];
        fgets(flag, sizeof(flag), fp);
        printf("Flag: %s\n", flag);

        fclose(fp);
    }
    else
    {
        printf("Nope, try again!\n");
    }

    cleanupProtocol(&pd);
    return 0;
}