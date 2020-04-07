import setuptools

setuptools.setup(
    name="cmapy",
    version="0.0.1",
    author="Stefan Dähling",
    author_email="SDaehling@eonerc.rwth-aachen.de",
    description="Python package for cloneMAP agents",
    url="https://git.rwth-aachen.de/acs/public/cloud/mas/cmapy",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'certifi==2019.11.28',
        'chardet==3.0.4',
        'idna==2.8',
        'paho-mqtt==1.5.0',
        'requests==2.22.0',
        'urllib3==1.25.8'
    ],
)