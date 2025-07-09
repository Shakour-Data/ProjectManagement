from setuptools import setup, find_packages

setup(
    name='auto_project_manager',
    version='0.1.0',
    description='A Python package for automated project management with GitHub and VS Code integration',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Add dependencies here, e.g. 'requests', 'flask', etc.
    ],
    entry_points={
        'console_scripts': [
            'auto-project-manager=cli:main',
        ],
    },
    python_requires='>=3.7',
)
