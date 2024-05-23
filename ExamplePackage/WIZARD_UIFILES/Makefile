include ../Makefile.inc

.PHONY: all install packageinstall clean

UIFILES = uninstall_uifile install_uifile

all install:
	/usr/local/tool/snpm i
	/usr/local/tool/snpm build

packageinstall: $(UIFILES)
	[ -d $(PKG_DIR)/WIZARD_UIFILES ] || install -d $(PKG_DIR)/WIZARD_UIFILES
	for i in $(UIFILES); do \
		install -c -m 644 $$i $(PKG_DIR)/WIZARD_UIFILES; \
	done

clean:
	@for i in $(UIFILES); do $(RM) $$i ; done

%: create_%.sh
	./$<
