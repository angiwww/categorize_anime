import os
import shutil
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("video_processing.log"),  # Save logs to a file
        logging.StreamHandler()  # Print logs to console
    ]
)
logger = logging.getLogger()

# Enter your directories for files
video_dir = "/volume1/Video/download"
final_dir = "/volume1/Video/TVAnime"
file_path = "/volume1/Video/download/videolist.txt"  # Specify the file path that stores files already processed

def get_video_files(file_path):
    """Reads the file and returns the list of previously processed video files."""
    try:
        with open(file_path, "r") as file:
            return file.read().splitlines()  # Read all lines and return as a list
    except FileNotFoundError:
        logger.error(f"The file {file_path} was not found.")
        return []
    except Exception as e:
        logger.error(f"An error occurred while reading {file_path}: {e}")
        return []

def write_video_file(file_path, video_file):
    """Appends a new video file name to the text file."""
    try:
        with open(file_path, "a") as file:
            file.write("\n" + video_file)
    except Exception as e:
        logger.error(f"Error writing to {file_path}: {e}")

def organize_videos():
    video_files_old = get_video_files(file_path)
    video_files = os.listdir(video_dir)

    for video_file in video_files:
        if video_file not in video_files_old:
            logger.info(f"Processing new video file: {video_file}")
            write_video_file(file_path, video_file)

            video_path = os.path.join(video_dir, video_file)
            video_extension = os.path.splitext(video_file)[1]

            try:
                name_and_episode = video_file.split('] ', 1)[1].split(' (', 1)[0]
                name = name_and_episode.split(' -')[0]

                copy_dir = os.path.join(final_dir, name)
                copy_path = os.path.join(copy_dir, name_and_episode + video_extension)

                # Create directory if it does not exist
                if not os.path.exists(copy_dir):
                    os.makedirs(copy_dir)

                # Copy the video file to the new directory
                shutil.copy(video_path, copy_path)
                logger.info(f"Copied {video_file} to {copy_path}")

            except IndexError:
                logger.warning(f"Skipping file {video_file} due to naming format issues.")
            except FileNotFoundError:
                logger.error(f"Source file {video_file} not found in {video_dir}.")
            except shutil.Error as e:
                logger.error(f"Error copying {video_file}: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred while processing {video_file}: {e}")

    logger.info("Finished processing all files.")

if __name__ == "__main__":
    organize_videos()
