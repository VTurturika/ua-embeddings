FROM tensorflow/tensorflow:latest-py3
WORKDIR /embeddings
CMD tensorboard --logdir wiki:log/wiki,potter:log/potter