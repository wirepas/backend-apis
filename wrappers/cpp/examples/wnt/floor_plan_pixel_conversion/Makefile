BINNAME = floor_plan_pixel_conversion
CC = gcc
CFLAGS = -g -O2 -Wall -Wextra

OBJECTS = main.o

all: $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) $(LDFLAGS) -o $(BINNAME)

main.o:
	$(CC) $(CFLAGS) -c main.c

clean:
	rm *.o
