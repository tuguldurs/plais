from setuptools import setup

setup(
    name='plais',
    version='0.0.1',
    packages=['plais'],
    install_requires=[
        'numpy>=1.22',
        'matplotlib>=3.5',
        'scikit-image>=0.19',
        'tqdm>=4.62',
        'imageio>=2.13',
        'imageio-ffmpeg>=0.4',
        'pyinstaller>=4.8',
        'gooey>=1.0.8'
    ],
    python_requires='>=3.7',
)
