# image_cartoonizer

This project has two objectives: (I) cartoonize images using traditional computer vision, then (II) train a cGAN to perform the same task. 

The project folders are structured in the following way;

data:

- cartoonized_images: This is the set of cartoonized images.
- cartoonized_with_cartoonizer_1: This is the set of images cartoonized with the first method of cartoonization.
- cartoonized_zith_cartoonizer_2: This is the set of images cartoonized with the second method of cartoonization.
- groundtruth_images: This is the set of original images with labels transformed.
- original_images: This is the set of raw images of the project.
- test: The set of cartoonized images for testing.
- train: The set of cartoonized images for training the model.

logs:

- cartoonize.log: Global monitoring of cartoonization process.
- split_by_cartoonization.log: Information about processes undergone in classifying images by cartoonization method used.
- train_test_split.log: Provides information about the train test split process.

scripts:

- `utils.py`: Defines helper functions that are used inside many scripts. Actually it contains only one function.
- `copy_and_rename.py`: This script renames the collected images from the `original_images` directory as `1.jpg`, `2.jpg`, `3.jpg`, ..., and save the renamed images inside `ground_truth_images`. 
- `cartoonization_methods.py`: Defines the different cartoonization methods that can be used. We implemented two of them: `cartoonizer_1` and `cartoonizer_2`.
- `cartoonize.py`: Runs the cartoonization on each image present in the `ground_truth_images` directory. Each image is randomly cartoonized by one of the methods defined in `cartoonization_methods.py` script. The results are stored in the directory called `cartoonized_images`.
- `split_by_cartoonization_method.py`: Split cartoonized images (stored in `cartoonized_images`) depending on the cartoonization method used to transform them. 
- `train_test_split.py`: Stacks each ground truth image and its cartoonized equivalent horizontally as the cGAN model we're going to use (pix2pix) suggests, stores the results in `transformed_images` directory, and splits those transformed images in train and test set, with a train size of 80%. The destination directories are named `train` and `test`.

`Image_to_cartoon_translation_with_a_conditional_GAN_(pix2pix).ipynb`: The notebook containing the modeling of cGAN.
