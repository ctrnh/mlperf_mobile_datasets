Script which converts a given dataset to imagenet/coco/ade20k-like dataset for testing MLPerf app.

# Requirements
- python3
- cv2
- matplotlib, numpy, json (TODO: remove?)

# Description
This script takes as input a source dataset (e.g. Google Open Images). It subsamples this dataset, keeping only images which have objects which class intersects with the target dataset, and images which have valid amount of number of bounding boxes (tries to match the distribution of number of bounding boxes in the target dataset).
it formats it so as to mimic the target dataset (e.g. "coco") for the mobile_app.
It replaces the existing annotation file from mobile_app with
a new annotation file (corresponding to the new dataset) having the same format.
Then it pushes images of the new dataset to the mobile phone.



# Datasets
Source dataset is the dataset that we take images from, it is to be converted so as to mimic the Target dataset
## Source dataset
Source dataset can be:
- google.py: source dataset class for Google open images. By default, it is taking the V6 validation dataset.
- ADE20K.py: source dataset class for ADE20K. !! It is written in the old version of mobile_dataset. To use this script, please reimplement the class !!

## Target dataset
- ADE20K_target.py: annotations are not implemented yet. Images are resized to 512x512.
- coco.py: target dataset (for number of bounding boxes per image, it mimics the distribution of coco val 2017 dataset). Images are resized to 300x300 (and bounding boxes are adapted) so as to follow the [mobile_app documentation](https://github.com/mlperf/mobile_app/blob/master/cpp/datasets/README.md).
- imagenet.py: target dataset for imagenet validation set


# How to run

## Commands
List of commands for using Google as classification test dataset in mobile app, with N=70 images:
1. Clone the script and the mobile_app repo
```
git clone https://github.com/mlperf/mobile_datasets.git
git clone https://github.com/mlperf/mobile_app.git
```

2. Connect your phone to your computer.
3. You can either download manually the Google Open Images to `path_to_google_dataset` and use the following command
```
python  ./mobile_datasets --input_data_path=path_to_google_dataset --N=70 --type=imagenet --mobile_app_path=./mobile_app --dataset=google

```
or if you don't, do not specify `input_data_path`. It will download the Open images in a temporary folder `./mobile_app/tmp_dataset_script`.
```
python  ./mobile_datasets --N=70 --type=imagenet --mobile_app_path=./mobile_app --dataset=google
```

After running this script, new images will be created in `./mobile_app/tmp_dataset_script/img` and pushed into your phone at `/sdcard/mlperf_datasets/imagenet`. The script will ask you at the end of the process if you want to delete `./mobile_app/tmp_dataset_script`.

The corresponding annotations will be saved at `/mobile_app/java/org/mlperf/inference/assets.imagenet_val.txt`.

3. You will then need to rebuild the app:
```
export ANDROID_HOME=Path/to/SDK # Ex: $HOME/Android/Sdk
export ANDROID_NDK_HOME=Path/to/NDK # Ex: $ANDROID_HOME/ndk/(your version)
cd mobile_app
bazel-2.2.0 build -c opt --cxxopt='--std=c++14' \
    --fat_apk_cpu=x86,arm64-v8a,armeabi-v7a \
    //java/org/mlperf/inference:mlperf_app
adb install -r bazel-bin/java/org/mlperf/inference/mlperf_app.apk
```

Those commands are run from the root folder when the directory structure is like this:

```
root/
│   mobile_datasets
└───mobile_app/
│   │   ...
│   └───java/org/mlperf/inference/assets/
│       │   imagenet_val.txt
│       │   coco_val.pbtxt
│       │   ...
```
