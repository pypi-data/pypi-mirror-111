import tensorflow as tf

import ffd.unet as unet
import ffd.pix2pix as pix2pix
from ffd.densenet.densenet import DenseNet

from ffd.flownet.src.flowlib import flow_to_image
from ffd.flownet.src.flownet_sd.flownet_sd import FlowNetSD  # Ok
from ffd.flownet.src.training_schedules import LONG_SCHEDULE
from ffd.flownet.src.net import Mode
from ffd.resunet import res_unet
from ffd.unetpp import get_unetpp
slim = tf.contrib.slim


# def get_resunet(inputs, layers):
#     return res_unet(inputs.size, config.filters, config.kernel_size,
#                      config.num_channels, config.num_classes)


def get_unetplus(inputs, layers):
    return get_unetpp(inputs=inputs)


def generator(inputs, layers, useunet=True,features_root=64, filter_size=3, pool_size=2, output_channel=3):
    if useunet:
        return unet.unet(inputs, layers, features_root, filter_size, pool_size, output_channel)
    else:
        return get_unetplus(inputs, layers)

def discriminator(inputs, num_filers=(128, 256, 512, 512)):
    logits, end_points = pix2pix.pix2pix_discriminator(inputs, num_filers)
    return logits, end_points['predictions']


def flownet(input_a, input_b, height, width, reuse=None):
    net = FlowNetSD(mode=Mode.TEST)
    # train preds flow
    input_a = (input_a + 1.0) / 2.0     # flownet receives image with color space in [0, 1]
    input_b = (input_b + 1.0) / 2.0     # flownet receives image with color space in [0, 1]
    # input size is 384 x 512
    input_a = tf.image.resize_images(input_a, [height, width])
    input_b = tf.image.resize_images(input_b, [height, width])
    flows = net.model(
        inputs={'input_a': input_a, 'input_b': input_b},
        training_schedule=LONG_SCHEDULE,
        trainable=False, reuse=reuse
    )
    return flows['flow']

def get_densenet(inputs, layers):
    net = DenseNet(growthRate=12, depth=100, reduction=0.5,
                            bottleneck=True, nClasses=100)
    return net



def initialize_flownet(sess, checkpoint):
    flownet_vars = slim.get_variables_to_restore(include=['FlowNetSD'])
    flownet_saver = tf.train.Saver(flownet_vars)
    print('FlownetSD restore from {}!'.format(checkpoint))
    flownet_saver.restore(sess, checkpoint)
