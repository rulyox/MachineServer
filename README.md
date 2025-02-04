# MachineServer

A Flask server that can serve ML models.

MachineServer is divided into two parts, Server and Model.

## Server

The server handles all user requests and sends commands to the model.

The server and model communicates through pipe.

## Model

Can use any ML model. (Actually, it doesn't have to be a ML model at all.)

In this example, [Basic Image Classification](https://www.tensorflow.org/tutorials/keras/classification) is used.

## Web API

### POST /train

Create child and train model.

* Request Body JSON
```json
{
    "epoch": 10
}
```

* Response JSON
```json
{
    "accuracy": "0.885200023651123"
}
```

### POST /evaluate

Evaluate model.

* Request Body JSON
```json
{
    "index": 10
}
```

* Response JSON
```json
{
    "result": "Coat 92%"
}
```

### POST /close

Close child.

* Response JSON
```json
{
    "result": "Child closed"
}
```
