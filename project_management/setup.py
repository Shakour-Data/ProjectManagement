from setuptools import setup, find_packages

setup(
    name='auto_pm',
    version='0.1.0',
    description='A Python package for automated project management with GitHub and VS Code integration',
    long_description='This package provides tools for automated project management including task prioritization, progress reporting, and integration with GitHub and VS Code.',
    long_description_content_type='text/plain',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'PyGithub',
        'pytest',
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'auto_pm=modules.cli:main',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
