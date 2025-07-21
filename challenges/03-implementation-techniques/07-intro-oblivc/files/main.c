#define PROTOCOL_NAME yao
#define __OBLIV__

#include <stdio.h>
#include <stdlib.h>
#include <obliv.h>

// 👇 Now available thanks to our Docker patch!
void revealOblivInt(int *dest, obliv int *src, int party);

void protocol(void *arg)
{
    ProtocolDesc *pd = (ProtocolDesc *)arg;
    int party = ocCurrentParty(pd);

    obliv int x = 0, y = 0;
    obliv int isEqual;

    // Each party provides their own input
    if (party == 1)
        x = 1337;
    if (party == 2)
        y = 1337;

    isEqual = (x == y);

    // Reveal only to party 1
    if (party == 1)
    {
        int result;
        revealOblivInt(&result, &isEqual, 1);
        printf("Are they equal? %s\n", result ? "YES" : "NO");
    }
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        fprintf(stderr, "Usage: %s <party (1 or 2)>\n", argv[0]);
        return 1;
    }

    int party = atoi(argv[1]);

    ProtocolDesc pd;
    protocolUseStdio(&pd);
    setCurrentParty(&pd, party);

    execYaoProtocol(&pd, protocol, &pd);
    cleanupProtocol(&pd);

    return 0;
}
