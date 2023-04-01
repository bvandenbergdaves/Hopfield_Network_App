# Hopfield_Image_Network
Discrete Hopfield Networks with visualization and image processing tools implemented in python using
(almost) exclusively numpy.

The application is implimented using an MVP architecture, much of the underlying functionality is
accessable via the command line UI. A user can edit a collection of images, and then train a hopfield
network to recognize sections of those images. Depending on the parameters entered, the appication may
take a very long time to run, though some guardrails are built in.

If too many patterns are generated, the network memories will tend to be unstable. Increase the
value of 'cutoff' to reduce patterns generated. The higher the cutoff, the more the algorithm
filters out potentially similar patterns that could confuse the network's training algorithm.
