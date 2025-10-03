
# DDPM core: schedules, forward/backward processes, sampling.

class DDPM:
    def __init__(self, model, cfg):
        raise NotImplementedError("Implement DDPM in src/diffusion/diffusion.py")

    def sample(self, class_id: int, n: int):
        raise NotImplementedError("Implement sample in src/diffusion/diffusion.py")
