# This file is placed in the Public Domain.

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='genocide',
    version='36',
    url='https://github.com/bthate/genocide',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="! Article 15. as it is intended - otp.informationdesk@icc-cpi.int - OTP-CR-117/19 !",
    long_description=read(),
    license='Public Domain',
    py_modules=["ob"],
    packages=["gcd"],
    zip_safe=True,
    scripts=["bin/gcd"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
 