from invoke import task


@task
def clean(c):
    c.run(r"find . -regex '^.*\(__pycache__\|\.py[co]\)$ ' -delete")
    c.run("find . -name '__pycache__' -type d -exec rm -rf {} +")
    c.run("rm -rf .coverage .pytest_cache .mypy_cache")


@task
def clobber(c):
    c.run("rm -rf .venv")
    c.run("rm -rf .python-version")


@task
def format(c):
    c.run("black .")
    c.run("isort --profile black .")
    c.run("ruff --fix .")


@task
def lint(c):
    c.run("black --check .")
    c.run("isort --profile black .")
    c.run("ruff check .")
    c.run("mypy .")


@task
def test(c):
    c.run("pytest")
