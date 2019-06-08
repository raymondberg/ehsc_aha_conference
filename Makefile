THIS_FILE := $(lastword $(MAKEFILE_LIST))

generate:
	pipenv run python generate_schedule.py

deploy:
	scp index.html ethicalhuman.org:public_html/aha2019/index.html

reload:
	@$(MAKE) -f $(THIS_FILE) generate
	@$(MAKE) -f $(THIS_FILE) deploy
