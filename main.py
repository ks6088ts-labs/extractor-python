import base64
import os
from typing import Annotated
from urllib.parse import urljoin

import fitz
import typer
from dotenv import load_dotenv
from openai import AzureOpenAI

app = typer.Typer()


def get_gpt4v_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.getenv("api_key"),
        api_version=os.getenv("api_version"),
        base_url=urljoin(
            os.getenv("azure_endpoint"),
            f"openai/deployments/{os.getenv('azure_deployment_gpt4v')}/extensions",
        ),
    )


def get_extra_body(use_vision_enhancements):
    if not use_vision_enhancements:
        return None
    return {
        "dataSources": [
            {
                "type": "AzureComputerVision",
                "parameters": {
                    "endpoint": os.getenv("azure_cv_endpoint"),
                    "key": os.getenv("azure_cv_api_key"),
                },
            }
        ],
        "enhancements": {"ocr": {"enabled": True}, "grounding": {"enabled": True}},
    }


@app.command()
def pdf2img(
    path_to_pdf="document.pdf",
    path_to_output="artifacts",
):
    pdf = fitz.open(path_to_pdf)
    for page_number, page in enumerate(pdf):
        # Generate a filename for the image (e.g., "page_1.png")
        image_filename = f"{path_to_output}/page_{page_number + 1}.png"

        # Convert the page to an image and save it
        pix = page.get_pixmap()
        pix.pil_save(image_filename)
        print(f"Page {page_number + 1} saved as {image_filename}")

    # Close the PDF document
    pdf.close()


@app.command()
def img2txt(
    system_prompt="You are a top quality image scanning machine.",
    prompt="Please describe the following input image in Japanese in detail.",
    path_to_image="image.png",
    use_vision_enhancements: Annotated[bool, typer.Option(help="Use vision enhancements for the image.")] = False,
):
    client = get_gpt4v_client()
    encoded_image = base64.b64encode(open(path_to_image, "rb").read()).decode("ascii")
    response = client.chat.completions.create(
        model=os.getenv("azure_deployment_gpt4v"),
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    },
                ],
            },
        ],
        max_tokens=2000,
        extra_body=get_extra_body(use_vision_enhancements),
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
