clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

run: clean
  ifdef HACKATHON
		echo $(HACKATHON)
		scrapy crawl projects -a hackathon=$(HACKATHON)
  else
		scrapy crawl projects -a hackathon=wirvsvirushackathon
  endif

requirements:
	pip install -r requirements.txt
	python3 -m spacy download en_core_web_sm
