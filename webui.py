import gradio as gr
from PIL import Image
import os
import shutil
from pathlib import Path
import shutil
from app_functions import *
# functions
model_choice = ["AnimeGANv3_Shinkai_37"]

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
                choosed_model = gr.Dropdown(
                    choices=model_choice, value=model_choice[0], label="选择使用的模型:"
                )
                
                save_v = gr.Button("save_video", variant="primary")
                with gr.Row():
                    transfer_v2v = gr.Button("开始风格转换", variant="primary")

            with gr.Column():
                video_output = gr.Video()
                video_text = gr.Textbox(label= "状态信息")



    transfer_p2p.click(
         fn=p2p_model_choice,
         inputs=[choosed_model],
         outputs=[image_output]
    )
    save.click(
        fn=save_image,
        inputs=[image_input],
        outputs=[text_output]
    )
    transfer_v2v.click(
        fn=v2v_model_choce,
        inputs=[choosed_model],
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
