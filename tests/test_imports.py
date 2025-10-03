
def test_imports():
    import src.data.prep as prep  # noqa: F401
    import src.gan.models as gan_models  # noqa: F401
    import src.diffusion.unet as unet  # noqa: F401
    assert True
