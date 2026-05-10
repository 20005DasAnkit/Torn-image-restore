import torch
import cv2
import numpy as np
import os

from .model import Generator


# DEVICE
device = torch.device("cpu")


# LOAD MODEL
model = Generator().to(device)

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "generator_gan_dwt_cpu.pth"
)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model.eval()


# 🔥 RESTORE FUNCTION
def restore_image(input_path, output_path):

    img = cv2.imread(input_path)

    if img is None:
        raise Exception("Image not found")

    original_h, original_w = img.shape[:2]

    # resize for model
    img = cv2.resize(img, (128, 128))

    img = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )

    tensor = (
        torch.tensor(img / 255.0)
        .permute(2, 0, 1)
        .unsqueeze(0)
        .float()
        .to(device)
    )

    # AI prediction
    with torch.no_grad():

        output = model(tensor)

    output_img = (
        output.squeeze()
        .permute(1, 2, 0)
        .cpu()
        .numpy()
    )

    output_img = (
        output_img * 255
    ).astype(np.uint8)

    # resize back
    output_img = cv2.resize(
        output_img,
        (original_w, original_h)
    )

    output_img = cv2.cvtColor(
        output_img,
        cv2.COLOR_RGB2BGR
    )

    # save image
    cv2.imwrite(
        output_path,
        output_img
    )

    return output_path