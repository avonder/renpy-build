from renpybuild.model import task

python2_version = "2.7.17"


@task(kind="python", pythons="2")
def unpack_python2(c):
    c.clean()

    c.var("version", python2_version)
    c.run("tar xzf {{source}}/Python-{{version}}.tgz")

    c.chdir("Python-{{ version }}")
    c.patch("{{ source }}/Python-{{ version }}-no-multiarch.diff")


@task(kind="python", pythons="2")
def build_python2(c):
    c.var("version", python2_version)

    c.chdir("Python-{{ version }}")

    with open(c.path("config.site"), "w") as f:
        f.write("ac_cv_file__dev_ptmx=no\n")
        f.write("ac_cv_file__dev_ptc=no\n")

    c.env("CONFIG_SITE", "config.site")

    c.env("CFLAGS", "{{ CFLAGS }} -DXML_POOR_ENTROPY=1 -DUSE_PYEXPAT_CAPI -DHAVE_EXPAT_CONFIG_H ")

    c.run("""./configure {{ config_cross }} --prefix="{{ install }}" --enable-ipv6""")

    c.copy("{{ source }}/Python-{{ version }}-Setup.local", "Modules/Setup.local")

    c.run("""{{ make }}""")
    c.run("""make altinstall""")

# @task(kind="python", pythons="2")
# def setup_python2(c):
#     c.var("version", python2_version)
#     c.chdir("Python-{{ version }}")
#     c.env("PYTHONPATH", ".")
#     c.run("""./python "{{source}}/all_modules_static.py" """)

