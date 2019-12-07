run: Architecture.py
	python3 Architecture.py inst.txt data.txt reg.txt config.txt result.txt
clean: 
	rm -f  *.pyc
	rm -r _pycache_
