EXEC=/bin/bash
PYEX=/usr/local/bin/python3
# The path to the pure data source code distribution
PDDIR=~/Development/pure-data
# The file name for the database
NAME=pddb.json
# The path to the current directory
CDIR=$(shell pwd)
# The path to the source code
SRCDIR=$(CDIR)/src
# The shell script
PDDB_MAKER=pddb.sh
# The pddb server
PDDB_SERVER=pddb.py
# The pddb client
PDDB_CLIENT=client.py
# The output database file
OUTPUT=$(CDIR)/$(NAME)
# -----------------------------------------------------------------------------
.SILENT:
all:
	cd $(SRCDIR); $(EXEC) $(PDDB_MAKER) $(PDDIR) $(OUTPUT)
	if [[ -f $(OUTPUT) ]]; then echo "Successfully created $(NAME)"; \
	else echo "Failed to create $(NAME)"; fi
start:
	@echo "Starting live database..."
	@echo "Type your queries, eg: osc~, and hit RETURN to get the result."
	@echo "Type QUIT and hit RETURN to quit."
	make server
	make client
server:
	@echo "Starting server..."
	$(PYEX) $(SRCDIR)/$(PDDB_SERVER) $(OUTPUT) &
client:
	@echo "Starting client..."
	$(PYEX) $(SRCDIR)/$(PDDB_CLIENT)
