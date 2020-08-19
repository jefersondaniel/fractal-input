from setuptools import setup
import fractal_input

long_description = open('README.rst', 'r').read()

setup(
    name='fractal_input',
    version=fractal_input.__version__,
    packages=['fractal_input'],
    setup_requires=['wheel'],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "fractal_input = fractal_input.__main__:__main__"
        ],
    },
    description="Abstracts HTTP request input handling, providing an easy interface for data hydration and validation",
    long_description=long_description,
    url='https://github.com/jefersondaniel/fractal-input',
    author='Jeferson Daniel',
    author_email='jeferson.daniel412@gmail.com',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
