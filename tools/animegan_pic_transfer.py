import subprocess
import sys
import os
import logging
import shutil
from tqdm import tqdm
def main():
    # 设置环境变量
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    # 在 Windows 终端中设置代码页为 UTF-8
    if os.name == 'nt':
        os.system('chcp 65001')
    
    """如果./workspace/output目录存在，删除该目录"""
    if os.path.exists("./workspace/output"):
        shutil.rmtree("./workspace/output")

    # 配置日志记录
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
        logging.StreamHandler(sys.stdout)
    ])

    logger = logging.getLogger()

    logger.info("在python脚本运行该指令")
    logger.info("output 编码为utf-8")

    """列出workspace/input目录下的文件"""
    files = os.listdir("./workspace/input")
    for file in tqdm(files):
        logger.info(file)
        result = subprocess.run(
            [sys.executable, "./tools/onnx_infer.py", "-i", f"./workspace/input/{file}", "-m", "./models/AnimeGANv3_Shinkai_37.onnx", "-o", "./workspace/output", "--background"],
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            universal_newlines=True
        )

        logger.info(result.stdout)
        logger.error(result.stderr)

if __name__ == "__main__":
    main()