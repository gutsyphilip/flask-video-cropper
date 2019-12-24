import cv2
import ffmpy
import uuid


class CropVideo:

    def __init__(self, start, duration, filepath):
        self.start_seconds = self.format_start(start)
        self.duration = duration
        self.filepath = filepath
        self.fps, self.width, self.height = self.get_fps()
        self.start_frames = round(self.fps * self.start_seconds)
        self.duration_frames = round(self.fps * duration)

    def get_fps(self):
        video = cv2.VideoCapture(self.filepath)
        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video.release()
        return fps, width, height

    def format_start(self, start_time):
        start_split = start_time.split(':')
        seconds = int(start_split[-1])
        minutes = int(start_split[-2])
        hours = int(start_split[-3])
        return (hours * 60 * 60) + (minutes * 60) + seconds

    def get_video(self):
        video = cv2.VideoCapture(self.filepath)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_filename = f'files/{str(uuid.uuid4())}.mp4'
        out = cv2.VideoWriter(output_filename, fourcc,
                              self.fps, (self.width, self.height))
        start_frame = self.start_frames
        end_frame = self.start_frames + self.duration_frames
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        while video.isOpened():
            ret, frame = video.read()
            if ret == True:
                if start_frame < end_frame:
                    out.write(frame)
                    start_frame += 1
                else:
                    break
            else:
                break

        video.release()
        out.release()
        cv2.destroyAllWindows()
        return output_filename

    def get_gif(self):
        outpath = self.get_video()
        gifpath = f'static/files/{str(uuid.uuid4())}.gif'
        ff = ffmpy.FFmpeg(
            inputs={outpath: None},
            outputs={gifpath: None}
        )
        ff.run()
        return gifpath
