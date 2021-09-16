#
#
# Anyscale CLI
#
# A brief tour
#
#


# You will not have to use the CLI.
# However, it provides an interface to Anyscale that is not
# fully replicated elsewhere, and so for the right workflows
# or for troubleshooting, the CLI can come in mighty handy.

# Projects/Working Directory
anyscale init -n my_new_project

# When you type this command, the CLI creates
# a file called .anyscale.yaml in the current directory.
# It also creates a project in your organization
cat .anyscale.yaml

cat ~/.anyscale/credentis.json

echo $ANYSCALE_CLI_TOKEN

# Danger: you can move this project file around.


# Cloud
# You use this command to associate Anyscale with AWS or GCP clouds
anyscale cloud

# Listing
anyscale list clouds
anyscale list ips
anyscale list projects

anyscale version

# running commands on a remote cluster
anyscale run

# On AWS (VMs) you can use this command to open a terminal session on your head node.
anyscale ssh

# To shut down a cluster, you can use
anyscale down

# The following commands operate on a slightly outdated notion of a project/working directory.  As long as you understand their behavior, you can use them to move files between your laptop and a running cluster's head node.

# This command pushes the contents of your working directory to Anyscale.
anyscale push
anyscale pull
anyscale clone


# Do not use the following commands.  
# They will not be supported in future versions of Anyscale:
autopush  Automatically synchronize a local project with a cluster.
up        Start or update a cluster based on the current...
exec      Execute shell commands in interactive cluster.
fork      Clones an existing cluster by name and initializes it
