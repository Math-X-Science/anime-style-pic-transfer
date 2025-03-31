from converter._path_parser import PathParser


def main():
    parser = PathParser()
    print(parser.ffmpeg)
    print(parser.ffprobe)
    print(parser.model_path)
    print(parser.realesr_excu)
    print(parser.realesr_model)
    print(parser.workspace)
    print(parser.input)
    print(parser.output)
    print(parser.tmp)
    print(parser.input_image)
    print(parser.output_image)
    print(parser.upscale_image)
    print(parser.input_video)
    print(parser.output_video)


if __name__ == "__main__":
    main()
