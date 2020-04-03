# Imports
from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import label_map_util
from object_detection.utils import ops as utils_ops
import cv2
import numpy as np
import os
import sys

# run on CPU
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import tensorflow as tf
from distutils.version import StrictVersion
from collections import defaultdict

# title of our window
title = "CAPTCHA"

# Env setup

# Model preparation
PATH_TO_FROZEN_GRAPH = 'inference_graph/frozen_inference_graph.pb'
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'training/labelmap.pbtxt'
NUM_CLASSES = 29


def decodeCaptcha(boxes, scores, classes, num_detections):
    list_x = []
    list_char = []
    for i in range(int(num_detections)):
        if scores[0][i] >= 0.8:
            temp = category_index.get(int(classes[0][i]))
            list_x.append(boxes[0][i][1])
            list_char.append(temp.get('name'))
            print(temp.get('name'), scores[0][i])

    list_x, list_char = zip(*sorted(zip(list_x, list_char)))
    return "".join(list_char)


# Load a (frozen) Tensorflow model into memory.
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)

categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


# Detection
def Captcha_detection(image):
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # Open image
            image_np = cv2.imread(image)
            # To get real color we do this:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            # Actual detection.
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name(
                'num_detections:0')
            # Visualization of the results of a detection.
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=2)

            # Show image with detection
            cv2.imshow(title, cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
            # cv2.imwrite("Predicted_captcha.jpg", cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))

            res = decodeCaptcha(boxes, scores, classes, num_detections)
            return res


if __name__ == '__main__':
    print(Captcha_detection("data/test/3y3x4.jpg"))
    # cv2.waitKey(0)
