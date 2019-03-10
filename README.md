# jbc
Jack's Blockchain -- Simple blockchain to learn and talk about how blockchains work.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

As always, you'll need to install the Python libraries in requirements.txt

```
$ pip install -r requirements.txt
```

### Running a node

To run the node on the command line, there are a few options.

`-m` tells the node to not only receive nodes, but also mine.

`-p PORT_NUM` will tell `node.py` which port to run on. This is important when running multiple nodes locally as described below.

### Hard linking directory for multiple nodes

In order to run a different node, we want to hard link the main jbc directory into another directory. To do this, use the [linknodes.sh](https://gist.github.com/jackschultz/5bdc628739c9ceae9ec96fadf9ed8557) script in the directory above jbc.

For example,

```
$ ./linknodes.sh 5001
```

will create a directory named `jbc5001`. Then in that directory, you'll be able to run a node on a different port to gather blocks or mine as well.

## Contributing

Feel free to clone, run, and give feedback and pull requests. Finding bugs is a great help to the project, as well as a great way for everyone to learn. And feel free to help update this README file to better describe how to run this locally.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
