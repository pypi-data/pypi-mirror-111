from setuptools import setup

setup(
    name='papago.py',
    version='0.1.0',
    author='Beta5051',
    author_email='beta5051@gmail.com',
    description='파이썬 네이버 파파고 API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Beta5051/papago.py',
    packages=['papago'],
    install_requires=['requests==2.25.1'],
    zip_safe=False,
)