BINNAME = floor_plan_pixel_conversion
CC = gcc
CFLAGS = -g -O2 -Wall -Wextra
LDFLAGS = -lm

OBJECTS = main.o

all: $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) -o $(BINNAME) $(LDFLAGS)

main.o:
	$(CC) $(CFLAGS) -c main.c

clean:
	rm *.o
