from setuptools import setup, find_packages

setup(
    name='plotdelice',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'scipy'
    ],
    entry_points={
        'console_scripts': [],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A package for creating customized  plots',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/daggermaster3000/plotdelice',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
