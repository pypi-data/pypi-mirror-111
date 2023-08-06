#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Codec wrapper for the Zstandard lossless image coder
"""

import os
import enb
from enb.config import options


class Zstandard(enb.icompression.LosslessCodec, enb.icompression.NearLosslessCodec, enb.icompression.FITSWrapperCodec):
    """Wrapper for the Zstandard codec
    All data types integer and float 16, 32, 64 can be compressed 
    """

    def __init__(self, compression_level='19', zstd_binary=os.path.join(os.path.dirname(__file__), "zstd")):
        """
        :param compression_level: 1-19, being 19 the maximum data reduction
        """
        super().__init__(compressor_path=zstd_binary,
                         decompressor_path=zstd_binary,
                         param_dict=dict(compression_level=compression_level))

    @property
    def name(self):
        """Don't include the binary signature
        """
        name = f"{self.__class__.__name__}{'__' if self.param_dict else ''}" \
               f"{'_'.join(f'{k}={v}' for k, v in self.param_dict.items())}"
        return name

    @property
    def label(self):
        return "Zstandard"

    def get_compression_params(self, original_path, compressed_path, original_file_info):
        return f"-{self.param_dict['compression_level']} -f {original_path}  -o {compressed_path}"

    def get_decompression_params(self, compressed_path, reconstructed_path, original_file_info):
        return f"-d -f {compressed_path} -o {reconstructed_path}"
