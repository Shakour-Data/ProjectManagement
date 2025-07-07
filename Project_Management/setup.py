from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Run the post install script
        subprocess.check_call([sys.executable, 'Project_Management/setup_post_install.py'])

setup(
    name='ProjectManagement',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'cryptography',
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'project_management=Project_Management.main:main',
        ],
    },
)
