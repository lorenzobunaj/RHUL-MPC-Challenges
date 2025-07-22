#define PROTOCOL_NAME yao
#define __OBLIV__

#include <obliv.h>
#include <stdio.h>
#include <stdlib.h>

// Only declare the minimal external libc functions
extern int fork(void);
extern unsigned int sleep(unsigned int seconds);
extern int wait(int *status);

// System headers needed for socket setup (safe for ARM builds)
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 54321 // Internal TCP port used between Party 1 and Party 2

// Forward declarations for patched obliv functions
void revealOblivInt(int *dest, obliv int *src, int party);
void feedOblivInt(obliv int *dest, int party, int value);

// Shared input/output structure for both parties
typedef struct
{
    obliv int guess;
    obliv int secret;
    obliv int match;
} ProtocolIO;

// The MPC program — compare guess and secret
void compare(void *args)
{
    ProtocolIO *io = args;
    io->match = (io->guess == io->secret);
}

// Internal Party 2 — runs as a child process and connects to Party 1
void runParty2()
{
    ProtocolDesc pd;
    ProtocolIO io;

    // Party 2 connects to Party 1's listening socket
    if (protocolConnectTcp2P(&pd, "127.0.0.1", "54321") != 0)
    {
        fprintf(stderr, "[P2] Connection failed\n");
        exit(1);
    }

    setCurrentParty(&pd, 2);
    feedOblivInt(&io.guess, 1, 0);     // Party 2 does not know the guess
    feedOblivInt(&io.secret, 2, 1337); // Hardcoded secret

    execYaoProtocol(&pd, compare, &io);
    cleanupProtocol(&pd);
    exit(0);
}

// Party 1 — this is the process the player connects to via netcat
int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        fprintf(stderr, "Usage: %s <party>\n", argv[0]);
        return 1;
    }

    int party = atoi(argv[1]);

    if (party == 1)
    {
        // Fork off Party 2 before doing anything else
        int pid = fork();
        if (pid < 0)
        {
            fprintf(stderr, "fork failed\n");
            return 1;
        }
        else if (pid == 0)
        {
            // Child: Party 2
            sleep(1); // Give Party 1 time to start listening
            runParty2();
        }

        // Parent: Party 1 — connected to netcat via stdin/stdout
        printf("Guess the number: ");
        fflush(stdout); // Make sure prompt reaches player

        int input;
        if (scanf("%d", &input) != 1)
        {
            fprintf(stderr, "Invalid input\n");
            return 1;
        }

        // Set up listening TCP socket on localhost:54321
        int server = socket(AF_INET, SOCK_STREAM, 0);
        if (server < 0)
        {
            perror("socket");
            return 1;
        }

        int opt = 1;
        setsockopt(server, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK); // 127.0.0.1
        addr.sin_port = htons(PORT);

        if (bind(server, (struct sockaddr *)&addr, sizeof(addr)) < 0)
        {
            perror("bind");
            return 1;
        }

        if (listen(server, 1) < 0)
        {
            perror("listen");
            return 1;
        }

        // Accept Party 2’s connection
        int client = accept(server, NULL, NULL);
        if (client < 0)
        {
            perror("accept");
            return 1;
        }

        // Initialize Obliv-C protocol using accepted socket
        ProtocolDesc pd;
        if (protocolAcceptTcp2P(&pd, client) != 0)
        {
            fprintf(stderr, "[P1] Accept failed\n");
            return 1;
        }

        setCurrentParty(&pd, 1);

        ProtocolIO io;
        feedOblivInt(&io.guess, 1, input); // Real guess from player
        feedOblivInt(&io.secret, 2, 0);    // Party 1 does not know the secret

        execYaoProtocol(&pd, compare, &io);

        int result = 0;
        revealOblivInt(&result, &io.match, 1); // Reveal result to Party 1

        if (result)
        {
            FILE *f = fopen("flag.txt", "r");
            if (f)
            {
                char flag[128];
                fgets(flag, sizeof(flag), f);
                printf("Flag: %s\n", flag);
                fclose(f);
            }
            else
            {
                printf("You got it, but no flag.txt\n");
            }
        }
        else
        {
            printf("Nope, try again!\n");
        }

        cleanupProtocol(&pd);
        wait(NULL); // Wait for child (Party 2) to finish
    }
    else
    {
        fprintf(stderr, "This binary is only meant to run with ./main 1 via socat\n");
        return 1;
    }

    return 0;
}