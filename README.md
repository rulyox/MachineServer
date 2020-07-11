# MachineServer

A Flask server that can serve ML models.

MachineServer is divided into two parts, Server and Model.

## Server

The server handles all user requests and sends commands to the model.

The server and model communicates through pipe.

## Model

Can use any ML model. (Actually, it doesn't have to be a ML model at all.)

In this example, [Basic Image Classification](https://www.tensorflow.org/tutorials/keras/classification) is used.
