import argparse
import sys
import tensorflow as tf


parser = argparse.ArgumentParser()
parser.add_argument('text', metavar='text', type=str, help='wiki|potter')
args = parser.parse_args()

if args.text != 'wiki' and args.text != 'potter':
    print('usage: python train.py wiki|potter')
    sys.exit(0)


def read_dictionary():
    with open('log/{0}/metadata.tsv'.format(args.text), 'r') as file:
        words = file.read().split()
        dictionary = {}
        for (i, word) in enumerate(words):
            dictionary[word] = i
        reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        return dictionary, reversed_dictionary


def get_test_words():
    with open('data/{0}/test_words'.format(args.text), 'r') as file:
        return file.read().split()


dictionary, reversed_dictionary = read_dictionary()


def get_nearest(embeddings, word=None, embedding=None):
    if word != None:
        word_embedding = tf.nn.embedding_lookup(embeddings, [dictionary.get(word, 0)])
    else:
        word_embedding = embedding
    similarity = tf.matmul(word_embedding, embeddings, transpose_b=True)
    sim = similarity.eval()
    nearest = (-sim).argsort()[0]
    return nearest[1:11]


with tf.Session() as sess:
    saver = tf.train.import_meta_graph('log/{0}/model.ckpt.meta'.format(args.text))
    saver.restore(sess, 'log/{0}/model.ckpt'.format(args.text))

    embeddings = tf.get_variable_scope().global_variables()[0]
    norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keepdims=True))
    normalized_embeddings = embeddings / norm

    if args.text == 'potter':
        harry = tf.nn.embedding_lookup(embeddings, [dictionary['гаррі']])
        he = tf.nn.embedding_lookup(embeddings, [dictionary['він']])
        she = tf.nn.embedding_lookup(embeddings, [dictionary['вона']])
        nearest = get_nearest(normalized_embeddings, embedding=harry - he + she)
        nearest_words = [reversed_dictionary[id] for id in nearest]
        print('Nearest to гаррі - він + вона: {0}'.format(', '.join(nearest_words)))

    test_words = get_test_words()
    for word in test_words:
        nearest = get_nearest(normalized_embeddings, word=word)
        nearest_words = [reversed_dictionary[id] for id in nearest]
        print('Nearest to {0}: {1}'.format(word, ', '.join(nearest_words)))

    print('Write search queries (type q for quit):')
    query = input('query = ')
    while query != 'q':
        query = query.lower()
        if dictionary.get(query, -1) != -1:
            nearest = get_nearest(normalized_embeddings, word=query)
            nearest_words = [reversed_dictionary[id] for id in nearest]
            print('Nearest to {0}: {1}'.format(query, ', '.join(nearest_words)))
        else:
            print('unknown word')
        query = input('query = ')

print('success')