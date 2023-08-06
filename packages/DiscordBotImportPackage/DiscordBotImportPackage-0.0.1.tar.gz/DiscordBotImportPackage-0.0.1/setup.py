from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='DiscordBotImportPackage',
    version='0.0.1',
    description='Just import this package and import all important packages for a Discord Bot with it!',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/WorldaDev',
    author='WorldaDev',
    author_email='worldadev@so-gehts.tk',
    license='MIT',
    classifiers=classifiers,
    keywords='discord, bot, dc',
    packages=find_packages(),
    install_requires=['']
)