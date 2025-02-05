import gradio as gr
from PIL import Image
import os
import shutil
from pathlib import Path
import shutil
from app_functions import *
# functions
"""模型选项"""
model_choice = ["AnimeGANv3_Shinkai_37"]
"""分辨率选项"""
resolution_choice = ["240p","720p"]
"""超分辨率选项"""
scale_choice = ["2x","4x"]


# UI排版
with gr.Blocks() as demo:
    with gr.Tab(label="image2image"):
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(
                )
                choosed_model = gr.Dropdown(
                    choices=model_choice, value=model_choice[0], label="选择使用的模型:"
                )
                resolution = gr.Dropdown(
                    choices=resolution_choice, value=resolution_choice[0], label="选择输出分辨率:"
                )
                # 勾选项，是否选择超分
                upscale_or_not = gr.Checkbox(label="是否进行超分", value=False)

                state = gr.State(value=0)
                save = gr.Button("save", variant="primary")
                with gr.Row():
                    transfer_p2p = gr.Button("开始风格转换", variant="primary")
                

            with gr.Column():
                with gr.Column():
                        image_output = gr.Image(label= "输出图片")

                        text_output = gr.Textbox(label= "状态信息")
    with gr.Tab(label="video2video"):
        with gr.Row():
            with gr.Column():
                video_input = gr.Video()
                choosed_model_v = gr.Dropdown(
                    choices=model_choice, value=model_choice[0], label="选择使用的模型:"
                )
                resolution_v = gr.Dropdown(
                    choices=resolution_choice, value=resolution_choice[0], label="选择输出分辨率:"
                )
                
                save_v = gr.Button("save_video", variant="primary")
                with gr.Row():
                    transfer_v2v = gr.Button("开始风格转换", variant="primary")

            with gr.Column():
                video_output = gr.Video()
                video_text = gr.Textbox(label= "状态信息")
                
    with gr.Tab(label="realesr-gan (testing)"):
        with gr.Row():
            with gr.Column():
                image_input_low_scale = gr.Image()
                image_scale = gr.Dropdown(
                    choices=scale_choice, value=scale_choice[1], label="选择超分倍率:"
                )
                with gr.Row():
                    upscale_p2p = gr.Button("开始超分", variant="primary")

            with gr.Column():
                video_output = gr.Image()
                video_text = gr.Textbox(label= "状态信息")




    transfer_p2p.click(
         fn=p2p_model_choice,
         inputs=[choosed_model,upscale_or_not],
         outputs=[image_output]
    )
    save.click(
        fn=save_image,
        inputs=[image_input,resolution],
        outputs=[text_output]
    )
    transfer_v2v.click(
        fn=v2v_model_choce,
        inputs=[choosed_model_v],
        outputs=[video_output]
    )
    save_v.click(
        fn=save_video,
        inputs=[video_input,resolution_v],
        outputs=[video_text]
    )
    upscale_p2p.click(
        fn=upscale_image,
        inputs=[image_input_low_scale,image_scale],
        outputs=[video_output]
    )


    
if __name__ == "__main__":

        print("推理页面已开启!")
        demo.launch()
