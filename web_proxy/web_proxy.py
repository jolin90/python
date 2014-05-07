#! /usr/bin/env python

import sys
import socket 
import thread
import select

network_protocol =  {
	"http"  : 80,
	"https" : 445,
	"ftp"   : 21,
}

def web_proxy_get_server_port(url_text):
	url_text_t  = url_text.split('/')

	url_text_t1 = url_text_t[2]
	url_text_t2 = url_text_t1.split(':')

	url_text_tt1 = url_text_t[0].split(':')

	if len(url_text_t2) == 2:
		port = url_text_t[2].split(':')[1]
	else :
		port = network_protocol[url_text_tt1[0]]
	
	return port

def network_parse_url(url):
	result1 = socket.getaddrinfo(url, None)
	result2 = result1[0][4]
	result3 = result2[0]
	return result3

def web_proxy_main_loop(src_socket, dest_socket, timeout=1, flag=2):
	inputs=[src_socket, dest_socket]  

	while True:   
		rs, ws, es=select.select(inputs, [], [])

		try:
			if src_socket in rs:
				buf_from_src = src_socket.recv(1024)
				if buf_from_src:
					dest_socket.send(buf_from_src)
				else:
					return -1
			elif dest_socket in rs:
				break
		except socket.error:
			return -2

	return 0

def del_string_message(string):

	buf1 = string.split('://')
	buf2 = buf1[1].split('/')[0]

	return  "%s://%s"  % (buf1[0], buf2)


def inet_init_socket(sock_client, flag):
	count = 0
	sock_inet = None
	host_url = None

	ret = 0;

	while True:
		count = count + 1
		try :
			messages = sock_client.recv(4096)
			if not messages: 
				ret = 1
				break

			message_t = messages.split()

			message_del="%s %s" % (message_t[0], del_string_message(message_t[1]))
			new_messages = "%s %s" % (message_t[0],	messages.split(message_del)[1])
			
			if not host_url:
				host_url = message_t[4]
			elif host_url != message_t[4]:
				sock_inet.close()
				sock_inet = None

			if not sock_inet:
				web_server_port = int(web_proxy_get_server_port(message_t[1]))
				web_server_ip = network_parse_url(message_t[4].split(':')[0])
				sock_inet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock_inet.connect((web_server_ip, web_server_port))

			sock_inet.send(new_messages)
			# print new_messages

			if web_proxy_main_loop(sock_client, sock_inet, 6, 0) < 0:
				break
			if web_proxy_main_loop(sock_inet, sock_client, 6, 1) < 0:
				break

		except socket.error:
			break

	if sock_client:
		sock_client.close()
	if sock_inet:
		sock_inet.close()
	
	print "\033[31mAccept end <<<< \033[0m"

def main(argv):
	port = 8989
	flag = 0
	if '-p' in argv:
		port=int(argv[argv.index('-p') + 1])
	if '--port' in argv:
		port=int(argv[argv.index('--port') + 1])

	sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_server.bind(("0.0.0.0", port))
	sock_server.listen(100)

	while True:
			print "\033[31mNew accept start >>>> \033[0m"
			connection, address = sock_server.accept()
			thread.start_new_thread(inet_init_socket, (connection, flag))
			flag = flag + 1

	sock_server.close()

if __name__ == '__main__':
	main(sys.argv)
