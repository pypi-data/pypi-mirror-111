import setuptools
import requests

resp = requests.get("https://github.com/Abdul-Muiz-Iqbal/Automaton/releases/latest")

VERSION = resp.url.split('/')[-1]

with open("README.md", "r") as f:
    desc = f.read()

setuptools.setup(
    name='automaton-linux',
    packages=setuptools.find_packages(),
    version=VERSION,
    license='MIT',
    description='An automation library for Linux using Uinput.',
    long_description =  desc,
    long_description_content_type = 'text/markdown',
    author='Abdul Muiz Iqbal',
    author_email='parkermuiz0@gmail.com',
    url='https://github.com/Abdul-Muiz-Iqbal/Automaton/',
    download_url=f'https://github.com/Abdul-Muiz-Iqbal/Automaton/archive/refs/tags/{VERSION}.tar.gz',
    keywords=['automation', 'linux', 'uinput'],
    install_requires=['evdev'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
