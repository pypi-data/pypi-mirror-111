from setuptools import setup

setup(
    name='msf_api',
    version='0.0.1',
    packages=['msf_api'],
    install_requires=[
        'requests',
        'requests-cache',
        'pydantic',
        'importlib; python_version == "3.8"',
    ],
)