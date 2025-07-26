#include "common.h"

void compare(void *args)
{
    ProtocolIO *io = args;
    io->match = (io->guess == io->secret);
}