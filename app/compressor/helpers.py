import subprocess
from datetime import timedelta


class MediaHelper:

    @staticmethod
    def compute_duration(file_path: str) -> str:
        """Returns media duration in seconds 00:00:00"""

        # ffprobe -i media_path  -show_entries  format=duration   -v quiet  -of   csv=p=0
        command = [
            "ffprobe",
            "-i",
            file_path,
            "-show_entries",
            "format=duration",
            "-v",
            "quiet",
            "-of",
            "csv=p=0",
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            duration: str = str(
                timedelta(seconds=float(result.stdout.strip()))
            )  # 00:00:00
            cleaned_duration = duration.split(".")[0]
            return cleaned_duration

    @staticmethod
    def generate_video_preview(
        input_file_path: str,
        video_name: str,
        output_folder: str,
        start_at: str = "00:00:00",
    ) -> str:
        """Returns the temporary path for the generated video preview"""
        # ffmpeg -i oop.mp4 -ss 00:00:05 -t 10  preview_oop.mp4
        video_preview_path = f"{output_folder}/video_preview_{video_name}.mp4"
        command = [
            "ffmpeg",
            "-i",
            input_file_path,
            "-ss",
            start_at,
            "-t",
            "10",  # 10th second from the start
            video_preview_path,
        ]
        result = subprocess.run(command, check=True, text=True)
        if result.returncode == 0:
            return video_preview_path

    @staticmethod
    def generate_video_thumbnail(
        input_file_path: str, output_folder: str, timestamp: str = "00:00:05"
    ) -> str:
        """Returns the temporary path for the generated video thumbnail"""
        # ffmpeg -i oop.mp4 -ss "00:00:05" -frames:v 1 oop-thumbnail.png
        thumbnail_path = f"{output_folder}/thumbnail.png"
        command = [
            "ffmpeg",
            "-i",
            input_file_path,
            "-ss",
            timestamp,
            "-frames:v",
            "1",
            thumbnail_path,
        ]
        result = subprocess.run(command, check=True, text=True)
        if result.returncode == 0:
            return thumbnail_path

    @staticmethod
    def compress_video(
        input_file_path: str, video_name: str, output_folder: str
    ) -> str:
        compressed_video_path = f"{output_folder}/compressed_version_{video_name}.mp4"
        command = ["ffmpeg", "-i", input_file_path, compressed_video_path]
        result = subprocess.run(command, check=True, text=True)
        if result.returncode == 0:
            return compressed_video_path

    @staticmethod
    def compress_audio(
        input_file_path: str, audio_name: str, output_folder: str
    ) -> str:
        compressed_audio_path = f"{output_folder}/compressed_version_{audio_name}.mp3"
        command = ["ffmpeg", "-i", input_file_path, compressed_audio_path]
        result = subprocess.run(command, check=True, text=True)
        if result.returncode == 0:
            return compressed_audio_path
