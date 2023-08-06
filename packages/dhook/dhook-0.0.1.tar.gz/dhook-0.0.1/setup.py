from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python'
]

setup(
    name='dhook',
    version='0.0.1',
    description='Discord Webhooks',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Ateş Selim Özgür',
    author_email='atesselimozgur@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='webhook',
    packages=find_packages(),
    install_requires=['requests']
)