


from __future__ import absolute_import, division, print_function, unicode_literals

# In[7]:


import tensorflow as tf

# In[8]:


import numpy as np

import matplotlib.pyplot as plt

import IPython.display as display
import PIL.Image

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)





frames = []




class DeepDream(tf.Module):
    def __init__(self, model):
        self.model = model

    @tf.function(
        input_signature=(
                tf.TensorSpec(shape=[None, None, 3], dtype=tf.float32),
                tf.TensorSpec(shape=[], dtype=tf.int32),
                tf.TensorSpec(shape=[], dtype=tf.float32),)
    )
    def __call__(self, img, steps, step_size):
        print("Tracing")
        loss = tf.constant(0.0)
        for n in tf.range(steps):
            with tf.GradientTape() as tape:
                # This needs gradients relative to `img`
                # `GradientTape` only watches `tf.Variable`s by default
                tape.watch(img)
                loss = calc_loss(img, self.model)

            # Calculate the gradient of the loss with respect to the pixels of the input image.
            gradients = tape.gradient(loss, img)

            # Normalize the gradients.
            gradients /= tf.math.reduce_std(gradients) + 1e-8

            # In gradient ascent, the "loss" is maximized so that the input image increasingly "excites" the layers.
            # You can update the image by directly adding the gradients (because they're the same shape!)
            img = img + gradients * step_size
            img = tf.clip_by_value(img, -1, 1)

        return loss, img








def random_roll(img, maxroll):
    # Randomly shift the image to avoid tiled boundaries.
    shift = tf.random.uniform(shape=[2], minval=-maxroll, maxval=maxroll, dtype=tf.int32)
    shift_down, shift_right = shift[0], shift[1]
    img_rolled = tf.roll(tf.roll(img, shift_right, axis=1), shift_down, axis=0)
    return shift_down, shift_right, img_rolled



class TiledGradients(tf.Module):
    def __init__(self, model):
        self.model = model

    @tf.function(
        input_signature=(
                tf.TensorSpec(shape=[None, None, 3], dtype=tf.float32),
                tf.TensorSpec(shape=[], dtype=tf.int32),)
    )
    def __call__(self, img, tile_size=512):
        shift_down, shift_right, img_rolled = random_roll(img, tile_size)

        # Initialize the image gradients to zero.
        gradients = tf.zeros_like(img_rolled)

        # Skip the last tile, unless there's only one tile.
        xs = tf.range(0, img_rolled.shape[0], tile_size)[:-1]
        if not tf.cast(len(xs), bool):
            xs = tf.constant([0])
        ys = tf.range(0, img_rolled.shape[1], tile_size)[:-1]
        if not tf.cast(len(ys), bool):
            ys = tf.constant([0])

        for x in xs:
            for y in ys:
                # Calculate the gradients for this tile.
                with tf.GradientTape() as tape:
                    # This needs gradients relative to `img_rolled`.
                    # `GradientTape` only watches `tf.Variable`s by default.
                    tape.watch(img_rolled)

                    # Extract a tile out of the image.
                    img_tile = img_rolled[x:x + tile_size, y:y + tile_size]
                    loss = calc_loss(img_tile, self.model)

                # Update the image gradients for this tile.
                gradients = gradients + tape.gradient(loss, img_rolled)

        # Undo the random shift applied to the image and its gradients.
        gradients = tf.roll(tf.roll(gradients, -shift_right, axis=1), -shift_down, axis=0)

        # Normalize the gradients.
        gradients /= tf.math.reduce_std(gradients) + 1e-8

        return gradients

    # In[18]:



def calc_loss(img, model):
    # Pass forward the image through the model to retrieve the activations.
    # Converts the image into a batch of size 1.
    img_batch = tf.expand_dims(img, axis=0)
    layer_activations = model(img_batch)
    if len(layer_activations) == 1:
        layer_activations = [layer_activations]

    losses = []
    for act in layer_activations:
        loss = tf.math.reduce_mean(act)
        losses.append(loss)

    return tf.reduce_sum(losses)



class dream:
    def __init__(self ):

        self.base_model = tf.keras.applications.InceptionV3(include_top=False, weights='imagenet')





    # Create the feature extraction model




    def run_deep_dream_with_octaves(self,img,  names = ['mixed0'],steps_per_octave=50, step_size=0.05,
                                    octaves=range(-2, 3), octave_scale=1.1):

        layers = [self.base_model.get_layer(name).output for name in names]
        dream_model = tf.keras.Model(inputs=self.base_model.input, outputs=layers)
        self.deepdream = DeepDream(dream_model)
        self.get_tiled_gradients = TiledGradients(dream_model)
        base_shape = tf.shape(img)
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = tf.keras.applications.inception_v3.preprocess_input(img)

        initial_shape = img.shape[:-1]
        img = tf.image.resize(img, initial_shape)
        for octave in octaves:
            # Scale the image based on the octave
            new_size = tf.cast(tf.convert_to_tensor(base_shape[:-1]), tf.float32) * (octave_scale ** octave)
            print(new_size)
            img = tf.image.resize(img, tf.cast(new_size, tf.int32))

            for step in range(steps_per_octave):
                gradients = self.get_tiled_gradients(img)
                grad = gradients*step_size
                img = img *(1 + grad ) + 0.5*grad
                img = tf.clip_by_value(img, -1, 1)

                if step % 100 == 0:
                    display.clear_output(wait=True)




                    plt.imshow(img )
                    plt.show()

                    print("Octave {}, Step {}".format(octave, step))

        result = self.deprocess(img)
        return result

    # Download an image and read it into a NumPy array.
    def download(self,url, max_dim=None):
        img = PIL.Image.open(url)
        if max_dim:
            img.thumbnail((max_dim, max_dim))
        return np.array(img)

    # Normalize an image
    def deprocess(self,img):
        img = 255 * (img + 1.0) / 2.0
        return tf.cast(img, tf.uint8)

    # Display an image
    def show(self,img):
        display.display(PIL.Image.fromarray(np.array(img)))


# Downsizing the image makes it easier to work with.


# ## Prepare the feature extraction model








#d = dream()
#name = 'img.jpg'

#orignal_img = d.download(name,max_dim=500)

#d.run_deep_dream_with_octaves(img = orignal_img)











