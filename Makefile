# The path to the pure data source code distribution
PDDIR=~/Development/pure-data
# The file name for the database
NAME=pddb.json
# -----------------------------------------------------------------------------
# Should not have to edit these:
# -----------------------------------------------------------------------------
EXEC=/bin/bash
# The path to the current directory
CDIR=$(shell pwd)
# The path to the source code
SRCDIR=$(CDIR)/src
# The shell script
PDDB_MAKER=pddb.sh
# The output file
OUTPUT=$(CDIR)/$(NAME)
# -----------------------------------------------------------------------------
.SILENT all:
	cd $(SRCDIR); $(EXEC) $(PDDB_MAKER) $(PDDIR) $(OUTPUT)
	if [[ -f $(OUTPUT) ]]; then echo "Successfully created $(NAME)"; \
	else echo "Failed to create $(NAME)"; fi