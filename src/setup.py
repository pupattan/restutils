from setuptools import setup

setup(
    name='restutils',
    version='2.0.0',
    packages=['restutils'],
    url='https://github.com/pupattan/restutils',
    license='MIT',
    install_requires=['ssl'],
    author='pulak pattanayak',
    author_email='pulak.pattanayak@gmail.com',
    description='Provides libraries for REST API applications',
    keywords="rest http",
    use_2to3=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
