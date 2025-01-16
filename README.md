## 环境:

* 你需要ffmpeg,ffprobe.exe,并且根据你的路径修改path.yaml中路径。

* 你需要自行下载onnx模型:

参见:

./model/download.md

./tools/core/model_core/download.md

* 你需要自行配置pytorch>=2.0.1的环境，然后:

```cmd
pip install -r requirements.txt
```

## 需要修改的地方:

* ffmpeg的路径。
* config/runtime/lm.txt中workspace的位置，绝对路径改到项目根目录

## 运行：

```cmd
python webui.py
```

如果你在用我打包的一键包，那么请双击这里不存在的`运行webui.bat`。然后进入弹出的网址。

## 我引用和参考的仓库：

[AnimeGANv3:使用 AnimeGANv3 制作自己的动画作品，包括将照片或视频制作成动画。](https://github.com/TachibanaYoshino/AnimeGANv3)

[Real-ESRGAN:Real-ESRGAN 旨在开发用于一般图像/视频修复的实用算法。](https://github.com/xinntao/Real-ESRGAN)

[UGATIT pytorch:用于图像到图像翻译的无监督生成注意网络与自适应层-实例规范化](https://github.com/znxlwm/UGATIT-pytorch)

[Vtuber_Tutorial:【教程】从零开始的自制Vtuber！](https://github.com/RimoChan/Vtuber_Tutorial)

