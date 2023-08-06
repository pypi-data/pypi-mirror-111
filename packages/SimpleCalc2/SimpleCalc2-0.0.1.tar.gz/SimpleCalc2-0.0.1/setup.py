from setuptools import setup, find_packages

classifiers = [
    #'Development status :: 5 - Production/Stable',
    #'Intended Audience :: Developers',
    #'Operating system :: Microsoft :: Windows :: Windows 10',
    #'License :: OSI Approved :: MIT License',
    #'Programming Language :: Python :: 3'
]

setup(
    name='SimpleCalc2',
    version='0.0.1',
    description='A very basic calculator for algebra problems.',
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Leonardo Ricci Mingani',
    author_email='leonardo.riccimingani@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keyword='calculator',
    pakages=find_packages(),
    install_requires=['']
)