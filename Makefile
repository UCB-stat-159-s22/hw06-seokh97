.PHONY : html html-hub all clean env

html: 
	jupyter-book build .

conf.py: _config.yml _toc.yml
	jupyter-book config sphinx .

html-hub: conf.py
	sphinx-build  . _build/html -D html_baseurl=${JUPYTERHUB_SERVICE_PREFIX}/proxy/absolute/8000
	cd _build/html
	python -m http.server
	@echo "Start the Python http server and visit:"
	@echo "https://stat159.datahub.berkeley.edu/user-redirect/proxy/8000/index.html"


all :
	jupyter execute index.ipynb

clean:
	rm figures/* audio/* _build/*

env :
	mamba env create -f environment.yml --name ligo
	conda activate ligo
	python -m ipykernel install --user --name ligo --display-name "LIGO Kernel"