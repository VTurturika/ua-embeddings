import tensorflow as tf


def read_dictionary():
    with open('log/potter/metadata.tsv', 'r') as file:
        words = file.read().split()
        dictionary = {}
        for (i, word) in enumerate(words):
            dictionary[word] = i
        reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        return dictionary, reversed_dictionary


def get_test_words():
    with open('log/potter/test_words.txt', 'r') as file:
        return file.read().split()


dictionary, reversed_dictionary = read_dictionary()


def get_nearest(embeddings, word):
    word_embedding = tf.nn.embedding_lookup(embeddings, [dictionary[word]])
    similarity = tf.matmul(word_embedding, embeddings, transpose_b=True)
    sim = similarity.eval()
    nearest = (-sim).argsort()[0]
    return nearest[1:11]


with tf.Session() as sess:
    saver = tf.train.import_meta_graph('log/potter/model.ckpt.meta')
    saver.restore(sess, 'log/potter/model.ckpt')

    embeddings = tf.get_variable_scope().global_variables()[0]
    norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keepdims=True))
    normalized_embeddings = embeddings / norm

    test_words = get_test_words()
    for word in test_words:
        nearest = get_nearest(normalized_embeddings, word)
        nearest_words = [reversed_dictionary[id] for id in nearest]
        print('Nearest to {0}: {1}'.format(word, ', '.join(nearest_words)))

print('success')