from setuptools import setup

setup(
    name='plais',
    version='0.0.1',
    packages=['plais'],
    install_requires=[
        'numpy>=1.17',
        'matplotlib>=3',
        'scikit-image>=0.18',
        'tqdm>4.62',
        'scikit-learn>=1.0',
        'pandas>=1.3',
        'imageio>=2.13'
    ],
    python_requires='>=3.7',
)
