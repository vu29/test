from setuptools import setup,find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Common functionality to share among different services in bidso'

setup(
    name = "comm_bidso",
    version=VERSION,
    author="Bidso Dev",
    author_email="vibhu.upamanyu@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['PyJWT==2.6.0','djangorestframework==3.14.0','Django==4.1.3']
)
