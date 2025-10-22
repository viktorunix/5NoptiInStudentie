

setup:
	( \
	python3 -m venv myenv && \
	source myenv/bin/activate && \
	python -m pip install pygame \
	)
build:
	gcc src/launcher.c

run:
	./a.out

clean:
	rm ./a.out