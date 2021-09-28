import array
from vision.ssd.vgg_ssd import create_vgg_ssd, create_vgg_ssd_predictor
from vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
from vision.ssd.mobilenetv1_ssd_lite import create_mobilenetv1_ssd_lite, create_mobilenetv1_ssd_lite_predictor
from vision.ssd.squeezenet_ssd_lite import create_squeezenet_ssd_lite, create_squeezenet_ssd_lite_predictor
from vision.ssd.mobilenet_v2_ssd_lite import create_mobilenetv2_ssd_lite, create_mobilenetv2_ssd_lite_predictor
from vision.ssd.mobilenetv3_ssd_lite import create_mobilenetv3_large_ssd_lite, create_mobilenetv3_small_ssd_lite
from vision.utils.misc import Timer
import cv2
import sys
from vision.utils.time_measure import MeasureTime

def shape_to_bytes(width, height):
    width_bytes = width.to_bytes(2, byteorder="little", signed=False)
    height_bytes = height.to_bytes(2, byteorder="little", signed=False)
    return width_bytes + height_bytes

# if len(sys.argv) < 5:
#     print('Usage: python run_ssd_example.py <net type>  <model path> <label path> <image path>')
#     sys.exit(0)
# net_type = sys.argv[1]
# model_path = sys.argv[2]
# label_path = sys.argv[3]
# image_path = sys.argv[4]

# class_names = [name.strip() for name in open(label_path).readlines()]

# if net_type == 'vgg16-ssd':
#     net = create_vgg_ssd(len(class_names), is_test=True)
# elif net_type == 'mb1-ssd':
#     net = create_mobilenetv1_ssd(len(class_names), is_test=True)
# elif net_type == 'mb1-ssd-lite':
#     net = create_mobilenetv1_ssd_lite(len(class_names), is_test=True)
# elif net_type == 'mb2-ssd-lite':
#     net = create_mobilenetv2_ssd_lite(len(class_names), is_test=True)
# elif net_type == 'mb3-large-ssd-lite':
#     net = create_mobilenetv3_large_ssd_lite(len(class_names), is_test=True)
# elif net_type == 'mb3-small-ssd-lite':
#     net = create_mobilenetv3_small_ssd_lite(len(class_names), is_test=True)
# elif net_type == 'sq-ssd-lite':
#     net = create_squeezenet_ssd_lite(len(class_names), is_test=True)
# else:
#     print("The net type is wrong. It should be one of vgg16-ssd, mb1-ssd and mb1-ssd-lite.")
#     sys.exit(1)
# net.load(model_path)

# if net_type == 'vgg16-ssd':
#     predictor = create_vgg_ssd_predictor(net, candidate_size=200)
# elif net_type == 'mb1-ssd':
#     predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)
# elif net_type == 'mb1-ssd-lite':
#     predictor = create_mobilenetv1_ssd_lite_predictor(net, candidate_size=200)
# elif net_type == 'mb2-ssd-lite' or net_type == "mb3-large-ssd-lite" or net_type == "mb3-small-ssd-lite":
#     predictor = create_mobilenetv2_ssd_lite_predictor(net, candidate_size=200)
# elif net_type == 'sq-ssd-lite':
#     predictor = create_squeezenet_ssd_lite_predictor(net, candidate_size=200)
# else:
#     predictor = create_vgg_ssd_predictor(net, candidate_size=200)

if len(sys.argv) < 2:
    print('Usage: python run_ssd_preprocess.py <image path>')
    sys.exit(0)
image_path = sys.argv[1]

orig_image = cv2.imread(image_path)
image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)

image_bin = image.tobytes()

# TCP Client
import socket

target_ip = "127.0.0.1"
target_port = 8080
buffer_size = 4096

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_client.connect((target_ip,target_port))

width = image.shape[0]
height = image.shape[1]

print("shape: {}x{}".format(width, height))

tcp_client.send(shape_to_bytes(width, height) + image_bin + b'\0')

response = tcp_client.recv(buffer_size)
print("[*]Received a response : {}".format(response))

# boxes, labels, probs = predictor.predict(image, 10, 0.4)
# 
# for i in range(boxes.size(0)):
#     box = boxes[i, :]
#     # cv2.rectangle(orig_image, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 4)
#     print(round(box[0].item()))
#     cv2.rectangle(
#         orig_image,
#         (round(box[0].item()), round(box[1].item())),
#         (round(box[2].item()), round(box[3].item())),
#         (255, 255, 0),
#         4
#     )
#     #label = f"""{voc_dataset.class_names[labels[i]]}: {probs[i]:.2f}"""
#     label = f"{class_names[labels[i]]}: {probs[i]:.2f}"
#     cv2.putText(orig_image, label,
#                 (round(box[0].item()) + 20, round(box[1].item()) + 40),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1,  # font scale
#                 (255, 0, 255),
#                 2)  # line type
# path = "run_ssd_example_output.jpg"
# t = MeasureTime('cv2.imwrite')
# cv2.imwrite(path, orig_image)
# t.stop()
# print(f"Found {len(probs)} objects. The output image is {path}")
