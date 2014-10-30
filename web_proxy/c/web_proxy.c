/*
 * 建立TCP server 并发服务器
 * 接受客户端发来的字符串并打印
 * BY zhang90
 * 2011-8-4
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <netdb.h>
#include <poll.h>


#define MAXLINE 1024
#define RECVLEN 2048
#define SERV_PORT 8888
#define LISTEN_NUM 10

#define error_quit(msg) \
	do {perror(msg); exit(EXIT_FAILURE);} while(0)

#define error_quit_pthread(msg) \
	do {perror(msg); pthread_exit(NULL);}while(0);

#define IS_NUMBER(c) ((c) >= '0' && (c) <= '9')
#define NELEM(a) (sizeof(a) / sizeof((a)[0]))

struct network_protocol
{
	const char *hostname;
	unsigned short port;
};

struct network_url
{
	char protocol[8];
	char port[8];
	char hostname[512];
};

pthread_mutex_t mutex;

ssize_t inet_send(int sockfd, const char *buff, size_t size)
{
	ssize_t wrlen;
	const char *buff_end;

	for (buff_end = buff + size; buff < buff_end; buff += wrlen)
	{
		wrlen = send(sockfd, buff, buff_end - buff, MSG_NOSIGNAL);
		if (wrlen <= 0)
		{
			return wrlen;
		}
	}

	return size;
}

static inline ssize_t inet_recv(int sockfd, void *buff, size_t size)
{
	return recv(sockfd, buff, size, MSG_NOSIGNAL);
}

static int web_proxy_main_loop(int srcfd, int destfd, int timeout)
{
	int ret;
	ssize_t rwlen;
	char buff[2048];
	struct pollfd pfds[2] =
	{
		{
			.fd = srcfd,
			.events = POLLIN
		},
		{
			.fd = destfd,
			.events = POLLIN
		}
	};

	while (1)
	{
		ret = poll(pfds, NELEM(pfds), timeout);
		if (ret <= 0)
		{
			if (ret < 0)
			{
				return ret;
			}

			return -1;
		}

		if (pfds[0].revents)
		{
			rwlen = inet_recv(srcfd, buff, sizeof(buff));
			if (rwlen <= 0 || inet_send(destfd, buff, rwlen) < rwlen)
			{
				return -1;
			}
		}

		if (pfds[1].revents)
		{
			break;
		}
	}

	return 0;
}

int network_get_port_by_url(const struct network_url *url)
{
	return 80;
}

int inet_create_tcp_link_by_addrinfo(struct addrinfo *info, unsigned short port, struct sockaddr_in *addr)
{
	int sockfd;

	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd < 0)
		return sockfd;

	while (info)
	{
		if (info->ai_family == AF_INET)
		{
			struct sockaddr_in *p = (struct sockaddr_in*)info->ai_addr;
			p->sin_port = htons(port);

			if (connect(sockfd, (struct sockaddr *)p, sizeof(struct sockaddr)) == 0 )
			{
				if (addr)
					addr->sin_addr.s_addr = p->sin_addr.s_addr;

				return sockfd;
			}
		}

		info = info->ai_next;
	}

	close(sockfd);
	return -1;
}

int inet_create_tcp_link(const char* hostname_t, unsigned short port)
{
	int ret ;
	int sockfd;

	struct sockaddr_in addr;
	char * hostname;

	struct addrinfo *result = NULL;
	struct addrinfo hints;

	if (strncmp(hostname_t, "localhost", strlen("localhost")) == 0)
	{
		hostname = "127.0.0.1";
	} else {
		hostname = (char *)hostname_t;
	}

	if (inet_aton(hostname, &addr.sin_addr))
	{
		addr.sin_family = AF_INET;
		addr.sin_port = htons(port);
		sockfd = 1;
	} else {

		memset(&hints, 0, sizeof(hints));
		hints.ai_family = AF_INET;
		hints.ai_socktype = SOCK_STREAM;
		hints.ai_flags = 0;
		ret = getaddrinfo(hostname, NULL, &hints, &result);
		if (ret < 0 || result == NULL)
		{
			return -1;
		}
		sockfd = inet_create_tcp_link_by_addrinfo(result, port, &addr);
		freeaddrinfo(result);
	}

	if (sockfd < 0)
		return sockfd;

//	printf("%s => %s:%d\n", hostname, inet_ntoa(addr.sin_addr), port);

	return sockfd;
}

char * network_prase_url(const char * text, struct network_url * url)
{
	int step = 0;
	char *p = url->hostname;
	char *p_end = p + sizeof(url->hostname);

	url->port[0] = 0;
	url->protocol[0] = 0;

	while (p < p_end)
	{
		switch (*text)
		{
		case 0 ... 31:
		case ' ':
		case '/':
			*p = 0;
			return (char *)text;

		case ':':
			*p = 0;

			if (step == 0 && strncmp("//", text + 1, 2) == 0)
			{
				text += 3;
				p = url->hostname;
				strncpy(url->protocol, url->hostname, sizeof(url->protocol));
			}
			else if (IS_NUMBER(text[1]))
			{
				text++;
				p = url->port;
				p_end = p + sizeof(url->port);
			}
			else
			{
				return NULL;
			}

			step++;
			break;

		default:
			*p++ = *text++;
		}
	}

	return NULL;
}

static inline void inet_close_tcp_socket(int sockfd)
{
	fsync(sockfd);
	shutdown(sockfd, SHUT_RDWR);
	close(sockfd);
}

int network_url_equals(const struct network_url *url1, const struct network_url *url2)
{
	if (strcmp(url1->hostname, url2->hostname))
	{
		return 0;
	}

	if (strcmp(url1->protocol, url2->protocol))
	{
		return 0;
	}

	return strcmp(url1->port, url2->port) == 0;
}





void * thread_socket(void *arg)
{
	int ret;
	char buff[RECVLEN], *buff_end, *url_text, *new_request = NULL;
	int connfd = *(int *)arg;
	int readlen = 0;
	int cmdlen = 0;

	struct network_url urls[2], *url = &urls[0], *url_bak = &urls[1];
	int proxy_sockfd = -1;

	free(arg);

	if (pthread_detach(pthread_self()) != 0 )  /* 分离线程 */
		error_quit_pthread("pthread_detach");

	memset(urls, 0, 2* sizeof(struct network_url));
	memset(buff, 0, RECVLEN);
	while(1)
	{
		readlen = read(connfd, buff, RECVLEN);
		if (readlen <= 0)
			break;

		buff[readlen] = 0;
		buff_end = buff + readlen;

		for (url_text  = buff; url_text < buff_end && *url_text != ' '; url_text++);

		cmdlen = url_text - buff;
		*url_text++ = 0;

		new_request = network_prase_url(url_text, &urls[0]);
		if (NULL == new_request)
			break;

		pthread_mutex_lock(&mutex);
//		printf("client request is:\n");
//		printf("%s\n", buff);

//		printf("%d \n", cmdlen);
//		printf("%s,%s,%s\n", urls[0].protocol, urls[0].hostname, urls[0].port);
		pthread_mutex_unlock(&mutex);

		if (proxy_sockfd < 0 || network_url_equals(url_bak, url) == 0)
		{
			if (proxy_sockfd > 0)
				inet_close_tcp_socket(proxy_sockfd);

			proxy_sockfd = inet_create_tcp_link(url->hostname, network_get_port_by_url(url));
			if (proxy_sockfd < 0)
				break;

			if (url == urls)
			{
				url_bak = urls;
				url =  url_bak + 1;
			} else {
				url = urls;
				url_bak = url + 1;
			}
		}

		new_request -= (cmdlen + 1);
		memcpy(new_request, buff, cmdlen);
		new_request[cmdlen] = ' ';

//		printf("new request is :\n");
//		printf("%s\n", new_request);

		readlen = inet_send(proxy_sockfd, new_request, buff_end - new_request);
		if (readlen < 0)
			break;

		ret = web_proxy_main_loop(connfd, proxy_sockfd, 60 * 1000);
		if (ret < 0)
			break;
		ret = web_proxy_main_loop(proxy_sockfd, connfd, 60 * 1000);
		if (ret < 0)
			break;

		memset(buff, 0, RECVLEN);
	}

	if(close(connfd) == -1)
		error_quit_pthread("close");

	return  NULL;
}

int main()
{
	int         socketfd, *connfd;
	socklen_t   clilen;
	struct      sockaddr_in myaddr, cliaddr;
	pthread_t   pthread_id;

	if (pthread_mutex_init(&mutex, NULL) < 0)
		error_quit("pthread_mutex_init");


	// create new socket
	if((socketfd = socket(PF_INET, SOCK_STREAM, 0)) < 0)
		error_quit("socket");

	// init server
	bzero(&myaddr, sizeof(struct sockaddr_in));
	myaddr.sin_family       = PF_INET;
	myaddr.sin_addr.s_addr  = htonl(INADDR_ANY);
	myaddr.sin_port         = htons(SERV_PORT);

	if (bind(socketfd, (struct sockaddr *)&myaddr, sizeof(myaddr)) < 0)
		error_quit("bind");

	if (listen(socketfd, LISTEN_NUM) < 0)
		error_quit("listen");

	clilen = 0;

	for(;;)
	{
		connfd  = (int *) malloc(sizeof(int));
		*connfd  = accept(socketfd, (struct sockaddr *)&cliaddr, &clilen);
		if( *connfd == -1 )
		{
			free(connfd);
			error_quit("accept");
		}

		if (pthread_create(&pthread_id, NULL, thread_socket, (void *)connfd) < 0)
			error_quit("pthread");
	}

	close(socketfd);
	return 0;

}
