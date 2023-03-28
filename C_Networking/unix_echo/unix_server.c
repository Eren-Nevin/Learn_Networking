#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <signal.h>

char SERVER_PATH[] = "./server_path";
const int BUF_SIZE = 128;
int sfd;
char message_buffer[BUF_SIZE];

void on_terminate(int signal){
    close(sfd);
    remove(SERVER_PATH);
    _exit(0);
}


int main(){
    struct sockaddr_un server_sock, client_sock;
    socklen_t len;

    signal(SIGINT, on_terminate);
    remove(SERVER_PATH);

    sfd = socket(AF_UNIX, SOCK_DGRAM, 0);

    memset(&server_sock, 0, sizeof(struct sockaddr_un));
    server_sock.sun_family = AF_UNIX;
    strncpy(server_sock.sun_path, SERVER_PATH, sizeof(server_sock.sun_path) - 1);
    bind(sfd, (struct sockaddr *) &server_sock, sizeof(struct sockaddr_un));

    for (;;){
       len = sizeof(struct sockaddr_un);
       int numRead = recvfrom(sfd, message_buffer, BUF_SIZE, 0, 
               (struct sockaddr *) &client_sock, &len);
       if (numRead > 0){
           printf("Message Recieved From: %s\n", client_sock.sun_path);
           for (int i=0; i<numRead; i++)
               *(message_buffer+i) = toupper(*(message_buffer+i));
           sendto(sfd, message_buffer, BUF_SIZE, 0, 
                   (struct sockaddr *) &client_sock, len);
           memset(message_buffer, 0, BUF_SIZE);
       }
    }
}
