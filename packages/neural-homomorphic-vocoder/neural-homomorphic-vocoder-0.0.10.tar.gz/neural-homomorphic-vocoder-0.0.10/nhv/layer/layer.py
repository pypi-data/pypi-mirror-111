#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2021 Kazuhiro KOBAYASHI <root.4mac@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvLayers(nn.Module):
    in_channels = 80
    conv_channels = 256
    out_channels = 222
    kernel_size = 3
    dilation_size = 1
    group_size = 8
    n_conv_layers = 3
    use_causal = False
    conv_type = "original"

    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            if k not in self.__class__.__dict__.keys():
                raise ValueError(f"{k} not in arguments {self.__class__}.")
            setattr(self, k, v)
        if self.conv_type == "ddsconv":
            self.net = self.ddsconv()
        elif self.conv_type == "original":
            self.net = self.original_conv()
        else:
            raise ValueError(f"Unsupported conv_type: {self.conv_type}")

    def forward(self, x):
        """
        x: (B, T, in_channels)
        y: (B, T, out_channels)
        """
        return self.net(x)

    def original_conv(self):
        modules = []
        modules += [
            Conv1d(
                self.in_channels,
                self.conv_channels,
                self.kernel_size,
                self.dilation_size,
                1,
                self.use_causal,
            ),
            nn.ReLU(),
        ]
        for i in range(self.n_conv_layers):
            modules += [
                Conv1d(
                    self.conv_channels,
                    self.conv_channels,
                    self.kernel_size,
                    self.dilation_size,
                    self.group_size,
                    self.use_causal,
                ),
                nn.ReLU(),
            ]
        modules += [
            Conv1d(
                self.conv_channels,
                self.out_channels,
                self.kernel_size,
                self.dilation_size,
                1,
                self.use_causal,
            ),
        ]
        return nn.Sequential(*modules)

    def ddsconv(self):
        modules = []
        modules += [
            Conv1d(
                in_channels=self.in_channels,
                out_channels=self.conv_channels,
                kernel_size=1,
                dilation_size=1,
                group_size=1,
                use_causal=self.use_causal,
            )
        ]
        for i in range(self.n_conv_layers):
            if self.dilation_size == 1:
                dilation_size = self.kernel_size ** i
            else:
                dilation_size = self.dilation_size ** i
            modules += [
                DepthSeparableConv1d(
                    channels=self.conv_channels,
                    kernel_size=self.kernel_size,
                    dilation_size=dilation_size,
                    use_causal=self.use_causal,
                )
            ]
        modules += [
            Conv1d(
                in_channels=self.conv_channels,
                out_channels=self.out_channels,
                kernel_size=1,
                dilation_size=1,
                group_size=1,
                use_causal=self.use_causal,
            )
        ]
        return nn.Sequential(*modules)


class Conv1d(nn.Module):
    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size=3,
        dilation_size=1,
        group_size=1,
        use_causal=False,
    ):
        super().__init__()
        self.use_causal = use_causal
        self.kernel_size = kernel_size
        self.padding = (kernel_size - 1) * dilation_size

        self.conv1d = nn.Conv1d(
            in_channels,
            out_channels,
            kernel_size,
            padding=self.padding,
            dilation=dilation_size,
            groups=group_size,
        )
        nn.init.kaiming_normal_(self.conv1d.weight)

    def forward(self, x):
        """
        x: (B, T, D)
        y: (B, T, D)
        """
        x = x.transpose(1, 2)
        y = self.conv1d(x)
        # NOTE(k2kobayashi): kernel_size=1 does not discard padding
        if self.kernel_size > 1:
            if self.use_causal:
                y = y[..., : -self.padding]
            else:
                y = y[..., self.padding // 2 : -self.padding // 2]
        return y.transpose(1, 2)


class DepthSeparableConv1d(nn.Module):
    def __init__(self, channels, kernel_size, dilation_size, use_causal=False):
        super().__init__()
        self.sep_conv = Conv1d(
            channels,
            channels,
            kernel_size,
            dilation_size,
            group_size=channels,
            use_causal=use_causal,
        )
        self.conv1d = Conv1d(
            channels,
            channels,
            kernel_size=1,
            dilation_size=1,
            group_size=1,
            use_causal=use_causal,
        )
        self.ln1 = nn.LayerNorm(channels)
        self.ln2 = nn.LayerNorm(channels)

    def forward(self, x):
        y = self.sep_conv(x)
        y = self.ln1(y)
        y = F.gelu(y)
        y = self.conv1d(y)
        y = self.ln2(y)
        y = F.gelu(y)
        return x + y


class DFTLayer(nn.Module):
    def __init__(self, n_fft=1024):
        super().__init__()
        self.n_fft = n_fft
        wsin, wcos = self._generate_fourier_kernels(n_fft=n_fft)
        self.register_buffer("wsin", torch.tensor(wsin, dtype=torch.float))
        self.register_buffer("wcos", torch.tensor(wcos, dtype=torch.float))

    @staticmethod
    def _generate_fourier_kernels(n_fft, window="hann"):
        freq_bins = n_fft
        s = np.arange(0, n_fft, 1.0)
        wsin = np.empty((freq_bins, 1, n_fft))
        wcos = np.empty((freq_bins, 1, n_fft))
        for k in range(freq_bins):
            wsin[k, 0, :] = np.sin(2 * np.pi * k * s / n_fft)
            wcos[k, 0, :] = np.cos(2 * np.pi * k * s / n_fft)
        return wsin.astype(np.float32), wcos.astype(np.float32)

    def forward(self, x, inverse=False):
        if inverse:
            return self.idft(x)
        else:
            return self.dft(x)

    def dft(self, x):
        if x.size(-1) != self.n_fft:
            raise ValueError("size mismatch between x.size(-1) and n_fft")
        if len(x.size()) == 3:
            bs = x.size(0)
            x = x.reshape(-1, 1, x.size(-1))
        else:
            bs = 0
            x = x.unsqueeze(1)
        imag = F.conv1d(x, self.wsin, stride=self.n_fft + 1)
        real = F.conv1d(x, self.wcos, stride=self.n_fft + 1)
        if bs != 0:
            imag = imag.reshape(bs, -1, x.size(-1))
            real = real.reshape(bs, -1, x.size(-1))
        return torch.complex(real, -imag).squeeze(-1)

    def idft(self, x):
        if len(x.real.size()) == 3:
            bs = x.real.size(0)
            real = x.real.reshape(-1, 1, self.n_fft)
            imag = x.imag.reshape(-1, 1, self.n_fft)
        else:
            bs = 0
            real = x.real.unsqueeze(1)
            imag = x.imag.unsqueeze(1)
        a1 = F.conv1d(real, self.wcos, stride=self.n_fft + 1)
        a2 = F.conv1d(real, self.wsin, stride=self.n_fft + 1)
        b1 = F.conv1d(imag, self.wcos, stride=self.n_fft + 1)
        b2 = F.conv1d(imag, self.wsin, stride=self.n_fft + 1)
        imag = a2 + b1
        real = a1 - b2
        if bs != 0:
            imag = imag.reshape(bs, -1, self.n_fft)
            real = real.reshape(bs, -1, self.n_fft)
        return torch.complex(real / self.n_fft, imag / self.n_fft).squeeze(-1)
