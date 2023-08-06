from setuptools import setup, find_packages



setup(
    name="sentinel-python",
    version="0.0.1",
    author="xezzz",
    description="Package for using Discord slash commands",
    packages=find_packages(),
    install_requires=["websocket-client"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)