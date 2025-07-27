#ifndef COMMON_H
#define COMMON_H

#define PROTOCOL_NAME yao
#define __OBLIV__

#include <obliv.h>

typedef struct
{
    obliv int guess;
    obliv int secret;
    obliv int match;
} ProtocolIO;

void compare(void *args);

#endif