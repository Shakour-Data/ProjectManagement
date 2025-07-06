from setuptools import setup, find_packages

setup(
    name='Project_Management',
    version='0.1.0',
    description='Automated Project Management Tool for Software Projects',
    author='Project Management Team',
    packages=find_packages(),
    install_requires=[
        'requests',
        'PyGithub',
        'flask',
        'pydantic',
    ],
    entry_points={
        'console_scripts': [
            'project_management=Project_Management.cli:main',
        ],
    },
    python_requires='>=3.8',
)
