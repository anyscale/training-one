This project contains training materials -- take 1

The three slide decks are snapshots of a particular set of sessions
from August-September 2021

```text
.
├── Makefile
├── README.md
├── TrainingNotebooks
│   ├── DevOps
│   ├── RayAndAnyscaleBasics
│   │   ├── 01-tasks.ipynb
│   │   ├── 01-tasks.py
│   │   ├── 02-actors.ipynb
│   │   ├── 02-actors.py
│   │   ├── 03-object-store.ipynb
│   │   ├── 03-object-store.py
│   │   ├── 04-scale.ipynb
│   │   ├── 04-scale.py
│   │   └── README.md
│   └── RaySGDandTune
│       ├── RaySGD.ipynb
│       └── RayTune.ipynb
├── requirements.txt
├── AnyscaleDevOps
│   ├── 01_cli_commands.sh
│   ├── 02_sdk.py
│   ├── 03_lifecycle.sh
│   ├── 04_ray_serve.py
│   ├── README.md
│   ├── app
│   │   ├── __init__.py
│   │   └── computation.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── anyscale_distributed.py
│       ├── local_distributed.py
│       ├── locustfile.py
│       └── units.py
└── scripts
    ├── build_new_env.py
    ├── mk_clusters.py
    ├── scratch.py
    └── test_driver.py
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



