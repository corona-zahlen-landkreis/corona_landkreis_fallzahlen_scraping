build:
	sudo docker build -t crawler .
run:
	sudo docker run -it --mount type=bind,src="$$(pwd)",destination=/landkreise crawler

.PHONY: build run
