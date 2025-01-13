# Copyright (c) 2000-2020 Synology Inc. All rights reserved.

## You can use CC CFLAGS LD LDFLAGS CXX CXXFLAGS AR RANLIB READELF STRIP after include env.mak
include /env.mak
EXEC= examplePkg
OBJS= examplePkg.o
all: $(EXEC)
$(EXEC): $(OBJS)
        $(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)
install: $(EXEC)
        mkdir -p $(DESTDIR)/usr/bin/
        install $< $(DESTDIR)/usr/bin/
clean:
        rm -rf *.o $(EXEC)
