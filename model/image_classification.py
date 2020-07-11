import sys
import tensorflow as tf
from tensorflow import keras
import numpy as np

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

model = None


def train():
    global model
    global train_images
    global test_images

    # preprocess
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    # build model
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10)
    ])

    # compile model
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )

    # train
    model.fit(train_images, train_labels, epochs=10)

    # evaluate
    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

    sys.stdout.write(f'accuracy:{test_acc}\n')
    sys.stdout.flush()


def predict(idx):
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    predictions = probability_model.predict(test_images)

    predictions_array = predictions[idx]
    return "{} {:2.0f}%".format(class_names[np.argmax(predictions_array)], 100 * np.max(predictions_array))


def get_input():
    while True:
        data = sys.stdin.readline()
        index = data.strip()

        if index == '':
            break

        result = predict(int(index))

        sys.stdout.write(f'{result}\n')
        sys.stdout.flush()


def main():
    train()
    get_input()


if __name__ == '__main__':
    main()
