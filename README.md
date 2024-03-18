[![test](https://github.com/ks6088ts-labs/extractor-python/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/extractor-python/actions/workflows/test.yaml?query=branch%3Amain)
[![docker](https://github.com/ks6088ts-labs/extractor-python/actions/workflows/docker.yaml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/extractor-python/actions/workflows/docker.yaml?query=branch%3Amain)
[![docker-release](https://github.com/ks6088ts-labs/extractor-python/actions/workflows/docker-release.yaml/badge.svg)](https://github.com/ks6088ts-labs/extractor-python/actions/workflows/docker-release.yaml)

# extractor-python

A data extract tool written in Python

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [GNU Make](https://www.gnu.org/software/make/)

## How to use

```shell
# Help
❯ python main.py --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  img2txt
  pdf2img

# Convert PDF document to images
❯ mkdir -p artifacts
❯ python main.py pdf2img \
    --path-to-pdf ./dataset/manual.pdf \
    --path-to-output ./artifacts
---
Page 1 saved as ./artifacts/page_1.png
Page 2 saved as ./artifacts/page_2.png
Page 3 saved as ./artifacts/page_3.png
Page 4 saved as ./artifacts/page_4.png
Page 5 saved as ./artifacts/page_5.png
Page 6 saved as ./artifacts/page_6.png
Page 7 saved as ./artifacts/page_7.png
Page 8 saved as ./artifacts/page_8.png
Page 9 saved as ./artifacts/page_9.png
Page 10 saved as ./artifacts/page_10.png

# Convert image to text using GPT-4 with vision enhancements
❯ python main.py img2txt \
    --system-prompt "You are a top quality image scanning machine." \
    --prompt "Please describe the following input image in Japanese in detail.", \
    --path-to-image "./artifacts/page_1.png" \
    --use-vision-enhancements
```

## Development instructions

### Local development

Use Makefile to run the project locally.

```shell
# help
make

# install dependencies for development
make install-deps-dev

# run tests
make test

# run CI tests
make ci-test
```

### Docker container

Use Docker to run the project in a container.

```shell
# run the container
docker run --rm ks6088ts/extractor-python python main.py --help

# go to the shell in the container
docker run --rm -it \
  -v $(pwd)/dataset:/app/dataset \
  -v $(pwd)/artifacts:/app/artifacts \
  -v $(pwd)/settings.env:/app/settings.env \
  ks6088ts/extractor-python \
  bash

# call convert PDF document to images
docker run --rm \
  -v $(pwd)/dataset:/app/dataset \
  -v $(pwd)/artifacts:/app/artifacts \
  -v $(pwd)/settings.env:/app/settings.env \
  ks6088ts/extractor-python \
  python main.py pdf2img --path-to-pdf /app/dataset/manual.pdf --path-to-output /app/artifacts

# call convert image to text using GPT-4 with vision enhancements
docker run --rm \
  -v $(pwd)/artifacts:/app/artifacts \
  -v $(pwd)/settings.env:/app/settings.env \
  ks6088ts/extractor-python \
  python main.py img2txt \
    --system-prompt "You are a top quality image scanning machine." \
    --prompt "Please describe the following input image in Japanese in detail." \
    --path-to-image /app/artifacts/page_1.png \
    --use-vision-enhancements
```
