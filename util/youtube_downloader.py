"""@package util
"""

import json
import os
from subprocess import DEVNULL, STDOUT, check_call

from pytube import YouTube


def get_frames(video, image_prefix, output_folder):
    """
    Extract the the frames from the video.

    :param video: to extract frames
    :param image_prefix: prefix for frames
    :param output_folder: to store frames
    """
    print("Frames will be generatet for {} in {}".format(video, output_folder))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # using ffmpeg to extract frames
    cmd = ["ffmpeg", "-y", "-i", video, "-r", "1", "-s", "224x224", "-f", "image2", "-sws_flags", "bilinear",
           os.path.join(output_folder, image_prefix + "_%03d.jpeg")]
    check_call(cmd, stdout=DEVNULL, stderr=STDOUT)


def trim(start, end, input, output):
    """
    Trims the input video and save it to the output

    :param start: time
    :param end: time
    :param input: video
    :param output: trimmed video
    """
    print("Video {} will be trimmet from {} to {}".format(input, start, end))
    # using ffmpeg to trim video
    cmd = ["ffmpeg", "-y", "-i", input, "-ss", "%0.2f" % start, "-to", "%0.2f" % end, output]
    check_call(cmd, stdout=DEVNULL, stderr=STDOUT)


def main():
    """
    Start downloading the youtube videos specified in the youtube_data.json. Trims the video and extract the frames.
    """
    print(os.getcwd())
    data_folder = 'data'
    download_dir = os.path.join(data_folder, "download")
    frames_dir = os.path.join(data_folder, "frames")

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    with open("util/youtube_data.json") as f:
        data_set = json.load(f)

    for key in data_set:
        label = data_set[key]["label"]
        video_name = label + "_" + key
        path_video = os.path.join(download_dir, video_name + ".mp4")
        path_video_short = os.path.join(download_dir, video_name + "_short.mp4")

        # download video from youtube if it does not exist
        if not os.path.exists(path_video):
            YouTube(data_set[key]["url"]).streams.first().download(output_path=download_dir, filename=video_name)

        # get start and end time to trim video
        start_time = data_set[key]["segment"][0]
        end_time = data_set[key]["segment"][1]

        # trim video
        trim(start_time, end_time, path_video, path_video_short)

        # get frames from video
        output_frame_folder = os.path.join(frames_dir, label)
        get_frames(path_video_short, key, output_frame_folder)


if __name__ == "__main__":
    main()
