# Hopfield_Image_Network
Discrete Hopfield Networks with visualization and image processing tools implemented in python using
(almost) exclusively numpy.

## Overview
The application is implimented using an MVP architecture, much of the underlying functionality is
accessable via the command line UI. A user can edit a collection of images, and then train a hopfield
network to recognize sections of those images. Depending on the parameters entered, the appication may
take a very long time to run, though some guardrails are built in.


## Cutoff Parameter
If too many patterns are generated, the network memories will tend to be unstable. Increase the
value of 'cutoff' to reduce patterns generated. The higher the cutoff, the more the algorithm
filters out potentially similar patterns that could confuse the network's training algorithm.


## Animations
Some example animations are provided in this repo. The black and white image on the left of each gif
represents the network state, while the blue and red image represents the network activation. The closer
to blue a neuron looks, the higher its activation, and the higher the chance that it will be in an on
state during the next iteration (if it is chosen to fire). The animation is intended to show the slow
convergence of the network towards a memorized pattern (the image segment) which is often evident in the
activation pattern of the neurons.
