# Anyscale init creates the file called .anyscale.yaml in this directory
# This file associates this directory with a project on Anyscale.
anyscale init

# You use this command to associate Anyscale with AWS or GCP clouds
anyscale cloud

# On AWS (VMs) you can use this command to open a terminal session on your head node.
anyscale ssh

# On AWS (VMs) this command pushes the contents of your working directory to Anyscale.
# It uses a pre-1.4.1 target directory
anyscale push




# There are several anyscale cli commands to avoid
  autopush  Automatically synchronize a local project with a cluster.
  clone     Clone a project that exists on anyscale, to your local machine.
  cloud     Configure cloud provider authentication for Anyscale.
  down      Stop the current cluster.
  exec      Execute shell commands in interactive cluster.
  fork      Clones an existing cluster by name and initializes it
  init      Create a new project or register an existing project.
  list      List resources (projects, clusters) within Anyscale.
  pull      Pull cluster
  push      Push current project to cluster.
  run       Run a shell command as a background job on anyscale.
  ssh       SSH into head node of cluster.
  up        DEPRECATED: Start or update a cluster based on the current...
  version   Display version of the anyscale CLI.
