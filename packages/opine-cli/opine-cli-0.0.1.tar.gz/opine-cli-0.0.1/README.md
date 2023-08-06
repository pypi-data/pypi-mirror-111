# OPINE CLI #

### What is this repository for? ###
This is a command line interface (CLI) for Opine.

### How do I get set up? ###
You can install `opine-cli` as a python package using `pip`.
* Installing from the PyPI package index:  
  `python -m pip install opine-cli`

* Install from the zipped distribution package:
  `python -m pip install <path/to/opine-cli-version.tar.gz>`

### Uninstall opine-cli ###

Run the command `python -m pip uninstall opine-cli`

### Using `opine-cli`
First ensure that you have installed the `opine-cli` package.

A few commands to get started with.

#### Initialize the cli
* `opine init` : Initialize the cli. 
    * This command uses the default opine api endpoint `https://api.opine.world`.
    * You can also specify an endpoint to use: `opine init https://my_other_endpoint.opine.
    world`
    * The init command also requests your user name and password to log you into Opine.
* `opine auth login`: To login explicitly.
* `opine auth revoke` : To logout and remove all user credentials.

#### Accessing projects
* `opine projects list` : Get a list of projects. You can use the `--output=FORMAT` flag to display the list in JSON format or as a table.
    * `opine projects list --output=json` : Format the results as json. This is the default.
    * `opine projects list --output=table` : Display the results as a table.
* `opine projects describe PROJECT-ID` : Get details of a project.
* `opine config set project_id PROJECT-ID` : Set the default project to query in the configuration file.
    * `opine projects describe` : If a PROJECT-ID is set in the config, then it can be omitted in the query above. In the documentation, use `[]` to indicate such optional attributes
* `opine projects stats [PROJECT-ID]` : Get projects statistics: number of forms, variable, data records and data values.
* `opine projects stats [PROJECT-ID]` : Get projects statistics: number of forms, variable, data records and data values.



### I need help. Who do I talk to? ###

* The Opine development team.