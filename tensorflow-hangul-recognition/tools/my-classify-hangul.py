#!/usr/bin/env python

import argparse
import io
import os
import sys

import tensorflow as tf

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

# My paths.
MY_LABEL_FILE = os.path.join(
    SCRIPT_PATH, '../labels/한국어 어휘 목록.txt'
)
MY_GRAPH_FILE = os.path.join(
    SCRIPT_PATH, '../my-saved-model/optimized_my_hangul_tensorflow.pb'
)


def my_read_image(file):
    file_content = tf.read_file(file)
    my_image = tf.image.decode_jpeg(file_content, channels=1)
    my_image = tf.image.convert_image_dtype(my_image, dtype=tf.float32)
    my_image = tf.reshape(my_image, (1, 64*64))
    return my_image


def my_classify(args):
    """Classify a character.

    This method will import the saved model from the given graph file, and will
    pass in the given image pixels as input for the classification. The top
    five predictions will be printed.
    """
    labels = io.open(args.label_file,
                     'r', encoding='utf-8').read().splitlines()

    if not os.path.isfile(args.image):
        print('Error: Image %s not found.' % args.image)
        sys.exit(1)

    # Load graph and parse file.
    with tf.gfile.GFile(args.graph_file, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    with tf.Graph().as_default() as graph:
        tf.import_graph_def(
            graph_def,
            input_map=None,
            return_elements=None,
            name='my-hangul-model',
            producer_op_list=None
        )

    # Get relevant nodes.
    x = graph.get_tensor_by_name('my-hangul-model/input:0')
    y = graph.get_tensor_by_name('my-hangul-model/output:0')
    keep_prob = graph.get_tensor_by_name('my-hangul-model/keep_prob:0')

    image = my_read_image(args.image)
    sess = tf.InteractiveSession()
    image_array = sess.run(image)
    sess.close()
    with tf.Session(graph=graph) as graph_sess:
        predictions = graph_sess.run(y, feed_dict={x: image_array,
                                                   keep_prob: 1.0})
        prediction = predictions[0]

    # Get the indices that would sort the array, then only get the indices that
    # correspond to the top 5 predictions.
    sorted_indices = prediction.argsort()[::-1][:5]
    for index in sorted_indices:
        label = labels[index]
        confidence = prediction[index]
        print('%s (confidence = %.5f)' % (label, confidence))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image', type=str,
                        help='Image to pass to model for classification.')
    parser.add_argument('--label-file', type=str, dest='label_file',
                        default=MY_LABEL_FILE,
                        help='File containing newline delimited labels.')
    parser.add_argument('--graph-file', type=str, dest='graph_file',
                        default=MY_GRAPH_FILE,
                        help='The saved model graph file to use for '
                             'classification.')
    my_classify(parser.parse_args())
