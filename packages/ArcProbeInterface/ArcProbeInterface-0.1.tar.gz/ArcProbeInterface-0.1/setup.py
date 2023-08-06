import setuptools

setuptools.setup(
    name="ArcProbeInterface",
    version="0.1",
    author="Thibault Buatois",
    author_email="thibaultbuatois@gmail.com",
    license="MIT License",
    description="Python API to use Redive Arcaea prober",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["websockets>=9.1", "websocket-client>=1.1.0", "brotli>=1.0.9"],
    python_requires=">=3.7",
    platform="any",
)
