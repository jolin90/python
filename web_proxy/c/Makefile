CC = gcc

CFLAGS =  -g -O2 -D_REENTRANT -Wall

LIBS = -lpthread 

PROGS = web_proxy

all: ${PROGS}

${PROGS}:web_proxy.o
	${CC} ${CFLAGS} -o $@ web_proxy.o ${LIBS} 

clean:
	rm *.o

disclean:
	rm *.o $(PROGS)
