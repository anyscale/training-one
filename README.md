This project contains

```
.
├── Makefile - used in post-install command to generate notebooks
├── example_compute_config.json
├── notebooks - the Makefile dumps notebooks in here.
├── scripts
│   ├── build_new_env.py - make a new cluster environment
│   ├── mk_clusters.py   - use a build id to spin up several clusters
│   ├── requirements.txt - not used yet
│   └── scratch.py       - to delete
└── src
    ├── actors.py        - lesson on actors
    ├── scale.py         - lesson on autoscaler sdk
    └── tasks.py         - lesson on tasks
```

the Makefile can be used to generate notebooks from the python files in src.
The environment build script r


