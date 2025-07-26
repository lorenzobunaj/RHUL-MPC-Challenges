#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "common.h"

extern void feedOblivInt(obliv int *dest, int party, int value);

int main()
{
    fprintf(stderr, "[P2] Starting Party 2\n");

    ProtocolDesc pd;
    ProtocolIO io;
    memset(&io, 0, sizeof(io));

    int retry = 5;
    while (protocolConnectTcp2P(&pd, "localhost", "54321") != 0 && retry-- > 0)
    {
        fprintf(stderr, "[P2] Retrying connection to Party 1... retries left: %d\n", retry);
        sleep(1);
    }
    if (retry < 0)
    {
        fprintf(stderr, "[P2] Connection to Party 1 failed\n");
        exit(1);
    }

    setCurrentParty(&pd, 2);
    fprintf(stderr, "[P2] Connected to Party 1\n");

    feedOblivInt(&io.guess, 1, 0);     // dummy
    feedOblivInt(&io.secret, 2, 1337); // actual secret

    execYaoProtocol(&pd, compare, &io);
    cleanupProtocol(&pd);
    return 0;
}