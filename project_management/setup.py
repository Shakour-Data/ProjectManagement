from setuptools import setup, find_packages

setup(
    name='project_management',
    version='1.0.0',
    description='Comprehensive Project Management Package',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(include=['project_management', 'project_management.*']),
    install_requires=[
        # Add any dependencies here
    ],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            # Add CLI entry points if needed
        ],
    },
)
