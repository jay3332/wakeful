from moviepy.editor import *

video = VideoFileClip(f"userfiles/797044260196319282.mp4")

txt_clip = ( TextClip("My Holidays 2013",fontsize=70,color='white')
             .set_position('center')
             .set_duration(10) )

result = CompositeVideoClip([video, txt_clip])
result.write_videofile(f"userfiles/797044260196319282.mp4")