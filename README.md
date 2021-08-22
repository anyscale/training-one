This project contains

```text
.
├── Makefile - `make` generates notebooks from python files
├── RayAndAnyscaleBasics - the Makefile dumps notebooks in here.
    ├── 01-tasks.py         - lesson on tasks
    ├── 02-actors.py        - lesson on actors
    ├── 03-object-store.py  - lesson on put and get
    ├── 04-scale.py         - lesson on autoscaler sdk
    └── requirements.txt    - not used yet
├── scripts
    ├── build_new_env.py - make a new cluster environment
    └── mk_clusters.py   - use a build id to spin up several clusters
```

The environment:

PROJECT_ID    Name of project called "RayAndAnyscaleBasics"
CPT_ID        A cluster compute for the training clusters
APT_ID        A cluster environment template.
ENV_FILE      Name of the environment file (so build ID can be written to it)
BUILD_ID      A build id to use.
STUDENTS      comma-delimited list of names to use in creating [clusters](clusters)


To launch a training environment (If you have a build ready)

* Activate an environment `. ./anyscale-env.sh`
* Launch clusters `python scripts/mk_clusters.py`

To prepare a build (if your git repo has been updated)

* run `python scripts/build_new_env.py`
* Activate the environment `. ./anyscale-env.sh`



