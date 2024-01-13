# RASA Project

This is a RASA project that uses the open source framework to build a contextual AI assistant.

## THINGS TO NOTE!!
The .env file that's needed to call the OpenWeather API is excluded from this repo since it's a private key. You can create a .env file in the actions folder
and use Python's os & dotenv library to access those files to call your SECRET_API keys. 
OS module is already installed in python & you can install dotenv using this command: _pip install python-dotenv_


## Installation

To install RASA and the required dependencies, run:

```bash
pip install rasa

Usage
To train a model, run:

rasa train

To test the model on the command line, run:

rasa shell

To run the action server, run:

rasa run actions

Testing
To evaluate the model performance, run:

rasa test

To run the end-to-end tests, run:

rasa test core --stories tests/test_stories.yml

Documentation
For more information on how to use RASA, please refer to the official documentation.

Contributing
We welcome contributions from the community. Please read the contributing guidelines before submitting a pull request.

License
This project is licensed under the Apache 2.0 License - see the LICENSE.txt file for details.

