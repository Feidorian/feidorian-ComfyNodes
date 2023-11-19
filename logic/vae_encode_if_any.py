import torch


class Feidorian_VAEEncodeIfAny:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { },
            "optional": {
            "pixels": ("IMAGE", ),
            "vae": ("VAE", )
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("Latent",)
    FUNCTION = "encode"

    CATEGORY = "feidorian/logic/latent"

    @staticmethod
    def vae_encode_crop_pixels(pixels):
        x = (pixels.shape[1] // 8) * 8
        y = (pixels.shape[2] // 8) * 8
        if pixels.shape[1] != x or pixels.shape[2] != y:
            x_offset = (pixels.shape[1] % 8) // 2
            y_offset = (pixels.shape[2] % 8) // 2
            pixels = pixels[:, x_offset:x + x_offset, y_offset:y + y_offset, :]
        return pixels

    @staticmethod
    def empty_latent(batch_size=1, height=512, width=512):
      latent = torch.zeros([batch_size, 4, height // 8, width // 8])
      return (latent,)

    def encode(self, vae=None, pixels=None):
        if(vae is None or pixels is None): return self.empty_latent()
        pixels = self.vae_encode_crop_pixels(pixels)
        t = vae.encode(pixels[:,:,:,:3])
        return ({"samples":t}, )

