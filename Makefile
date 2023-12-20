lint:
	poetry run ruff .
	poetry run pymarkdown --disable-rules MD041 scan README.md
	@# MD041 rule: first line in file should be a top level heading / unnecessary for docs

fmt:
	poetry run ruff . --fix

migrations:
	alembic revision --autogenerate

migrate:
	alembic upgrade head
rbmigrate:
	alembic downgrade base
