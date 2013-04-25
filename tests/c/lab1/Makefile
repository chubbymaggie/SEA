CFLAGS	:= -m32 -g -std=c99 -fno-stack-protector -Wall -Werror -D_GNU_SOURCE=1
LDFLAGS	:= -m32
PROGS	:= httpd-exstack httpd-nxstack

all:	$(PROGS) shellcode.bin

httpd:	httpd.o
	gcc $< -o $@ $(LDFLAGS)

%-exstack: %
	cp $< $@
	execstack -s $@

%-nxstack: %
	cp $< $@
	execstack -c $@

%.o:	%.c
	gcc $< -c -o $@ $(CFLAGS)

%.o:	%.S
	gcc $< -c -o $@ $(CFLAGS)

%.bin:	%.o
	objcopy -S -O binary -j .text $< $@

clean:
	rm -f *.o *.pyc *.bin httpd $(PROGS)

lab%-handin.tar.gz: clean
	tar cf - `find . -type f | grep -v '^\.*$$' | grep -v '/CVS/' | grep -v '/\.svn/' | grep -v '/\.git/' | grep -v 'lab[0-9].*\.tar\.gz'` | gzip > $@

handin: lab1-handin.tar.gz
	@echo "Please visit http://pdos.csail.mit.edu/cgi-bin/893handin"
	@echo "and upload $<.  Thanks!"

.PRECIOUS: %.o
