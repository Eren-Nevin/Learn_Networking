#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <netinet/in.h> 
#include <arpa/inet.h>
#include <netdb.h>

char SERVER_HOSTNAME[] = "localhost";
char SERVER_PORT[] = "52011";

const int BUF_SIZE = 128;
char message[BUF_SIZE];

int connection_socket;

void on_terminate(int signal){
    close(connection_socket);
    _exit(0);
}

int main(int argc, char **argv){
    struct sockaddr server_address;
    socklen_t len = sizeof(struct sockaddr);

    signal(SIGINT, on_terminate);

    connection_socket = socket(AF_INET, SOCK_STREAM, 0);

    // Get Server Address 
    struct addrinfo server_info_hint;
    memset(&server_info_hint, 0, sizeof(struct addrinfo));

    server_info_hint.ai_flags = AI_NUMERICSERV;
    server_info_hint.ai_family = AF_INET;
    server_info_hint.ai_socktype = SOCK_STREAM;

    struct addrinfo *result;
    int error = getaddrinfo(SERVER_HOSTNAME, SERVER_PORT, &server_info_hint, &result);
    server_address = *(result->ai_addr);


    // Connect To Server
    connect(connection_socket, &server_address, len); 

    for (;;){
        // Read Message From Stdin
        fgets(message, BUF_SIZE, stdin);

        // Send Message To Server
        write(connection_socket, message, BUF_SIZE);

        // Zero Out Message Buffer
        memset(message, 0, BUF_SIZE);

        // Recieve Response From Server
        int numRead = read(connection_socket, message, BUF_SIZE);
        
        // Check If Server Is Disconnected
        if (numRead <= 0){
            close(connection_socket);
            return 0;
        }

        // Printout Response To Stdout
        printf("%s", message);

        // Zero Out Message Buffer
        memset(message, 0, BUF_SIZE);
    }
}
