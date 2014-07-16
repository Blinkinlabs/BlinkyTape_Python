from setuptools import setup, find_packages

scripts = [
    'LEDWeather', 'binary_clock', 'flash_example', 'scanline', 'show_mode'
]

setup(
    name='BlinkyTape',
    version='0.1.0',
    description='Python module and example for the BlinkyTape.',
    long_description=(
        '\n\n'.join((open('README.md').read(), open('AUTHORS.md').read()))
    ),
    url='http://blinkinlabs.com/blinkytape/',
    license='MIT',
    author='Matthew Mets',
    author_email='web@cibomahto.com',
    install_requires=['pyserial', 'argparse'],
    packages=find_packages(),
    scripts=scripts,
    include_package_data=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
