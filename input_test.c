#include <sys/select.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/unistd.h>
#include <sys/ioctl.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>


void wait() {
    fd_set rfds;
    struct timeval tv;

    FD_ZERO(&rfds);
    FD_SET(STDIN_FILENO, &rfds);

    /* Wait up to five seconds. */
    tv.tv_sec = 5;
    tv.tv_usec = 0;

    int n = select(
        STDIN_FILENO+1,
        &rfds,
        NULL,
        NULL,
        &tv
    ); 

    printf("select()=%d\ntv_sec=%ld\ntv_usec=%ld\n",n,tv.tv_sec,tv.tv_usec);
    char buf[1];
    ssize_t size=read(STDIN_FILENO,buf,1);
    printf("read()=%ld\nbuf='%s'\n\n",size,buf);
}

int main() {
    wait();
    wait();
    return 0;
}