from fabric import task

@task
def python(c):
    c.run("python --version")
    c.run("python3 --version")
    c.run("which python")
    c.run("which python3")
