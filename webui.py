import gradio as gr
from PIL import Image
import os
import shutil
from pathlib import Path
import shutil
from app_functions import *
# functions
radio = ("x4","x8")
languages = ("3:4","16:9")

# UI排版
with gr.Blocks() as demo:
    with gr.Tab(label="image2image"):
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(
                )
                upscale_radio = gr.Dropdown(
                    choices=radio, value=radio[0], label="超分辨率缩放比"
                )
                scale = gr.Dropdown(
                    choices=languages, value=languages[0], label="人物截取比例"
                )

                state = gr.State(value=0)
                save = gr.Button("save", variant="primary")
                with gr.Row():
                    uga_trans = gr.Button("UGATIT 去背景人物转绘", variant="primary")
                    sd_trans = gr.Button("Stable Diffusion 去背景人物转绘", variant="primary")
                

            with gr.Column():
                with gr.Column():


                        image_output = gr.Image(label= "输出图片")

                        text_output = gr.Textbox(label= "状态信息")
    with gr.Tab(label="video2video"):
        with gr.Row():
            with gr.Column():
                video_input = gr.Video()
                upscale_radio = gr.Dropdown(
                    choices=radio, value=radio[0], label="超分辨率缩放比"
                )
                
                save_v = gr.Button("save_video", variant="primary")
                with gr.Row():
                    uga_v2v = gr.Button("UGATIT 去背景人物转绘", variant="primary")
                    sd_v2v = gr.Button("Stable Diffusion 去背景人物转绘", variant="primary")

            with gr.Column():
                video_output = gr.Video()
                video_text = gr.Textbox(label= "状态信息")



    uga_trans.click(
         fn=UGATIT_origin_bacground_transfer,
         inputs=[],
         outputs=[image_output]
    )
    sd_trans.click(
         fn=SD_origin_background_transfer,
         inputs=[],
         outputs=[image_output]
    )

    save.click(
        fn=save_image,
        inputs=[image_input],
        outputs=[text_output]
    )
    
    uga_v2v.click(
        fn=UGATIT_original_background_video_transfer,
        inputs=[],
        outputs=[video_output]
    )
    sd_v2v.click(
        fn=SD_origin_background_video_transfer,
        inputs=[],
        outputs=[video_output]
    )
    save_v.click(
        fn=save_video,
        inputs=[video_input],
        outputs=[video_text]
    )


    
if __name__ == "__main__":

        print("推理页面已开启!")
        demo.launch()
