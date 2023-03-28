#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <signal.h>
#include <netinet/in.h> 
#include <arpa/inet.h>
#include <netdb.h>

char SERVER_HOSTNAME[] = "localhost";
char SERVER_PORT[] = "52011"; 

const int BUF_SIZE = 128;
char message_buffer[BUF_SIZE];

const int BACKLOG = 50;
int listen_socket;

void on_terminate(int signal){
    close(listen_socket);
    _exit(0);
}

int main(){
    struct sockaddr server_address;
    struct sockaddr_in client_address;
    socklen_t len = sizeof(struct sockaddr_in);

    signal(SIGINT, on_terminate);

    // Open Socket
    listen_socket = socket(AF_INET, SOCK_STREAM, 0);

    // Construct Server Address Structure
    
    struct addrinfo server_info_hint;
    memset(&server_info_hint, 0, sizeof(struct addrinfo));
    server_info_hint.ai_flags = AI_NUMERICSERV;
    server_info_hint.ai_family = AF_INET;
    server_info_hint.ai_socktype = SOCK_STREAM;

    struct addrinfo *result;
    int error = getaddrinfo(SERVER_HOSTNAME, SERVER_PORT, &server_info_hint, &result);
    server_address = *(result->ai_addr);

    // Bind Socket 
    bind(listen_socket, &server_address, sizeof(struct sockaddr));

    // Make Socket Passive
    listen(listen_socket, BACKLOG);

    // Accept Connection On New Socket
    int new_socket = accept(listen_socket, (struct sockaddr *) &client_address, &len);

    // Print Client Info
    char client_host_name[NI_MAXHOST];
    char client_service_name[NI_MAXSERV];
    getnameinfo((struct sockaddr *) &client_address, len,
            client_host_name, NI_MAXHOST,
            client_service_name, NI_MAXSERV,
            NI_NUMERICSERV);
    printf("Connected From %s:%s\n", client_host_name, client_service_name);

    for (;;){

        // Read Request
        int numRead = read(new_socket, message_buffer, BUF_SIZE);
        if (numRead > 0){
            // Transform Message
            for (int i=0; i<numRead; i++)
                *(message_buffer+i) = toupper(*(message_buffer+i));

            // Send Back Response To Client
            write(new_socket, &message_buffer, BUF_SIZE);

            // Reset Message Buffer
            memset(message_buffer, 0, BUF_SIZE);
        }
        else {
            close(new_socket);
            close(listen_socket);
            return 0;
        }
    }
}
