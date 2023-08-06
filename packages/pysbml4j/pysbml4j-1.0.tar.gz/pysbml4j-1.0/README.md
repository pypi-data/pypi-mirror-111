[![Documentation Status](https://readthedocs.org/projects/pysbml4j/badge/?version=latest)](https://pysbml4j.readthedocs.io/en/latest/?badge=latest)
# SBML4j python package

This is the python package to talk to a running SBML4j service instance.

## Install
This package is available through pip (Currently only on the test instance)
To install use:
	
	pip install --index-url https://test.pypi.org/simple/ pysbml4j==0.1.17

## Usage
In your python project use
	 
>	import pysbml4j
>
>	client = pysbml4j.Sbml4j()

This generates a client connection to a server running on

	http://localhost:8080

To connect to a server running at different host use the 'Configuration' class

	config = pysbml4j.Configuration("http://my-server-url:port")
	client = pysbml4j.Sbml4j(config)

Then you can communicate with the running service using the client object.

	client.listNetworks()

The main working object then is the 'Network' class.

	myNet = client.getNetworkByName("NetworkNameFromNetworkList")

The following chapter describes the current options you have for working with the network element

### Working with a network

### Basic information
You can get a basic information dictionary for a network with

	myNetInfo = myNet.getInfoDict()

### GraphML

To get a graphML Representation use:

	graphMLString = myNet.graphML()
	
You can provide the 'directed' attribute (true, false) to determine whether the resulting graph should be directed or not. The default is 'false'


There are more options, which I will provide documentation for shortly.
Stay tuned.

To find out more about SBML4j visit the [kohlbacherlab github repository](https://github.com/kohlbacherlab/sbml4j.git)


