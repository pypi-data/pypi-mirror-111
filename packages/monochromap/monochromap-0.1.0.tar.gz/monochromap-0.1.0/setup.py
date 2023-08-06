from setuptools import setup

setup(
    name='monochromap',
    packages=['monochromap'],
    version='0.1.0',
    description='A highly opinionated way to paint and plot black and white map',
    author='M Iqbal Tawakal',
    author_email='mit.iqi@gmail.com',
    url='https://github.com/mitbal/monochromap',
    keywords='static map image osm',
    classifiers=[],
    install_requires=[
        'Pillow',
        'requests',
        'futures;python_version<"3.2"'
    ]
)
