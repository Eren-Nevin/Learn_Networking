#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>

int sfd;
char SERVER_PATH[] = "./server_path";
char CLIENT_PATH[] = "./client_path";
int BUF_SIZE = 128;

void on_terminate(int signal){
    close(sfd);
    remove(CLIENT_PATH);
    _exit(0);
}

int main(int argc, char **argv){
    struct sockaddr_un client_sock, server_sock;

    signal(SIGINT, on_terminate);

    remove(CLIENT_PATH);
    sfd = socket(AF_UNIX, SOCK_DGRAM, 0);

    memset(&client_sock, 0, sizeof(struct sockaddr_un));
    client_sock.sun_family = AF_UNIX;
    strncpy(client_sock.sun_path, CLIENT_PATH, sizeof(client_sock.sun_path) - 1);

    bind(sfd, (struct sockaddr *) &client_sock, sizeof(struct sockaddr_un));

    memset(&server_sock, 0, sizeof(struct sockaddr_un));
    server_sock.sun_family = AF_UNIX;
    strncpy(server_sock.sun_path, SERVER_PATH, sizeof(server_sock.sun_path) - 1);
    
    char message[BUF_SIZE];

    for (;;){
        socklen_t len = sizeof(struct sockaddr_un);
        fgets(message, BUF_SIZE, stdin);
        sendto(sfd, message, sizeof(message), 0, (struct sockaddr *) &server_sock, len);
        recvfrom(sfd, message, sizeof(message), 0, (struct sockaddr *) &server_sock, &len);
        printf("%s", message);
        memset(message, 0, BUF_SIZE);
    }
}
