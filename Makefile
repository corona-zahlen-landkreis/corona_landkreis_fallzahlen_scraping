build:
	sudo docker build -t district -f  Dockerfile .
run:
	sudo docker run -it --rm -v "$(CURDIR):/source:rw" --userns host district /bin/bash -i
run-ns:
	sudo docker run -it --rm -v "$(CURDIR):/source:rw" district /bin/bash -i
