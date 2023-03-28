#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <signal.h>
#include <netinet/in.h> 
#include <arpa/inet.h>

char SERVER_IP_STRING[] = "127.0.0.1";
int SERVER_PORT = 52011; 

const int BUF_SIZE = 128;
char message_buffer[BUF_SIZE];

int sfd;

void on_terminate(int signal){
    close(sfd);
    _exit(0);
}

int main(){
    struct sockaddr_in server_address, client_address;
    socklen_t len;

    signal(SIGINT, on_terminate);

    // Open Socket
    sfd = socket(AF_INET, SOCK_DGRAM, 0);

    // Construct Server Address Structure
    struct in_addr ip_address;
    inet_pton(AF_INET, SERVER_IP_STRING, &ip_address);
    server_address.sin_family = AF_INET;
    server_address.sin_port = SERVER_PORT;
    server_address.sin_addr = ip_address;

    // Bind Socket 
    bind(sfd, (struct sockaddr *) &server_address, sizeof(struct sockaddr_in));

    for (;;){
       len = sizeof(struct sockaddr_in);
       // Wait For Message
       int numRead = recvfrom(sfd, message_buffer, BUF_SIZE, 0, 
               (struct sockaddr *) &client_address, &len);
       if (numRead > 0){
           // Get Client Info
           char client_ip_string[INET_ADDRSTRLEN];
           struct in_addr client_ip_address = client_address.sin_addr;
           in_port_t client_port = client_address.sin_port;
           inet_ntop(AF_INET, &client_ip_address, client_ip_string, INET_ADDRSTRLEN);
           // Print Client Info
           printf("Message Recieved From: %s:%d\n", client_ip_string, client_port); 
           // Transform Message
           for (int i=0; i<numRead; i++)
               *(message_buffer+i) = toupper(*(message_buffer+i));
           // Send Back Response To Client
           sendto(sfd, message_buffer, BUF_SIZE, 0, 
                   (struct sockaddr *) &client_address, len);
           // Reset Message Buffer
           memset(message_buffer, 0, BUF_SIZE);
       }
    }
}
