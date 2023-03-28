#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <netinet/in.h> 
#include <arpa/inet.h>

char SERVER_IP_STRING[] = "127.0.0.1";
in_port_t SERVER_PORT = 52011;

char message[BUF_SIZE];
int BUF_SIZE = 128;

int sfd;

void on_terminate(int signal){
    close(sfd);
    _exit(0);
}

int main(int argc, char **argv){
    struct sockaddr_in server_address;

    signal(SIGINT, on_terminate);

    sfd = socket(AF_INET, SOCK_DGRAM, 0);

    // Construct Server Address Structure
    struct in_addr server_ip;
    inet_pton(AF_INET, SERVER_IP_STRING, &server_ip);
    server_address.sin_family = AF_INET;
    server_address.sin_port = SERVER_PORT;
    server_address.sin_addr = server_ip;


    for (;;){
        socklen_t len = sizeof(struct sockaddr_in);
        // Read Message From Stdin
        fgets(message, BUF_SIZE, stdin);

        // Send Message To Server
        sendto(sfd, message, sizeof(message), 0, (struct sockaddr *) &server_address, len);

        // Recieve Response From Server
        recvfrom(sfd, message, sizeof(message), 0, (struct sockaddr *) &server_address, &len);

        // Printout Response To Stdout
        printf("%s", message);

        // Zero Out Message Buffer
        memset(message, 0, BUF_SIZE);
    }
}
