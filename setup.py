from setuptools import setup, find_packages

setup(
    name='Lanai',
    packages=find_packages(exclude=['tests']),
    tests_require=['pytest'],
    install_requires=[
        'gevent==1.0.1',
        'greenlet==0.4.5',
        'PyYAML==3.11',
        'redis==2.10.3',
    ]
)
