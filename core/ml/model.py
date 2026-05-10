import torch
import torch.nn as nn


# CONV BLOCK
class ConvBlock(nn.Module):

    def __init__(self, in_channels, out_channels):

        super().__init__()

        self.block = nn.Sequential(

            nn.Conv2d(
                in_channels,
                out_channels,
                kernel_size=3,
                padding=1
            ),

            nn.BatchNorm2d(out_channels),

            nn.ReLU(inplace=True),

            nn.Conv2d(
                out_channels,
                out_channels,
                kernel_size=3,
                padding=1
            ),

            nn.BatchNorm2d(out_channels),

            nn.ReLU(inplace=True)

        )

    def forward(self, x):

        return self.block(x)


# GENERATOR
class Generator(nn.Module):

    def __init__(self):

        super().__init__()

        # ENCODER
        self.enc1 = ConvBlock(3, 32)

        self.pool1 = nn.MaxPool2d(2)

        self.enc2 = ConvBlock(32, 64)

        self.pool2 = nn.MaxPool2d(2)

        # BRIDGE
        self.bridge = ConvBlock(64, 128)

        # DECODER
        self.up2 = nn.ConvTranspose2d(
            128,
            64,
            kernel_size=2,
            stride=2
        )

        self.dec2 = ConvBlock(128, 64)

        self.up1 = nn.ConvTranspose2d(
            64,
            32,
            kernel_size=2,
            stride=2
        )

        self.dec1 = ConvBlock(64, 32)

        # FINAL
        self.final = nn.Conv2d(
            32,
            3,
            kernel_size=1
        )

    def forward(self, x):

        # ENCODER
        e1 = self.enc1(x)

        p1 = self.pool1(e1)

        e2 = self.enc2(p1)

        p2 = self.pool2(e2)

        # BRIDGE
        b = self.bridge(p2)

        # DECODER
        u2 = self.up2(b)

        u2 = torch.cat([u2, e2], dim=1)

        d2 = self.dec2(u2)

        u1 = self.up1(d2)

        u1 = torch.cat([u1, e1], dim=1)

        d1 = self.dec1(u1)

        # OUTPUT
        out = self.final(d1)

        return torch.sigmoid(out)