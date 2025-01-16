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

## 怎么玩：

建议先玩 image2image 和 realesr-gan。  

realesr-gan 我还没写2x的部分，所以暂时只能用4x。  

image2image 建议勾选超分，效果更佳。  

image2image 的输出分辨率可能让人混淆。实际上是指在不同的精度上对图片进行转换，实测较低的分辨率可以让图片细节变少，更接近油画，而分辨率越高，则越写实。（勾上超分进行的测试。）

### 示例

**原图:**

![image-20250116120008451](https://fastly.jsdelivr.net/gh/MrXnneHang/blog_img/BlogHosting/img/25/01/202501161200503.png)

**240p+超分:**

![image-20250116120059030](https://fastly.jsdelivr.net/gh/MrXnneHang/blog_img/BlogHosting/img/25/01/202501161201422.png)

**720p+超分:**

![image-20250116120134334](https://fastly.jsdelivr.net/gh/MrXnneHang/blog_img/BlogHosting/img/25/01/202501161201417.png)

按理来说，如果一直提高或者降低这个精度，比如送入64p的图片可能可以达到接近像素画的效果。

而一直提高这个精度，可能画出来的图片就会和原图几乎一模一样。

这个值得探索一下。但需要该点代码。后续可能会把这个输出分辨率设成一个可拖动的滑块，自由设置。


ps: video2video 暂未接入超分选项，以及还未测试，不建议尝试。

## 我引用和参考的仓库：

[AnimeGANv3:使用 AnimeGANv3 制作自己的动画作品，包括将照片或视频制作成动画。](https://github.com/TachibanaYoshino/AnimeGANv3)

[Real-ESRGAN:Real-ESRGAN 旨在开发用于一般图像/视频修复的实用算法。](https://github.com/xinntao/Real-ESRGAN)

[UGATIT pytorch:用于图像到图像翻译的无监督生成注意网络与自适应层-实例规范化](https://github.com/znxlwm/UGATIT-pytorch)

[Vtuber_Tutorial:【教程】从零开始的自制Vtuber！](https://github.com/RimoChan/Vtuber_Tutorial)

