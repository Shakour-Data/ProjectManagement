import os
import subprocess
import sys
import pytest
import setup_initialization

def test_create_virtualenv():
    env_dir = 'test_venv'
    if os.path.exists(env_dir):
        subprocess.call(['rm', '-rf', env_dir])
    setup_initialization.create_virtualenv(env_dir)
    assert os.path.exists(env_dir)
    # Clean up
    subprocess.call(['rm', '-rf', env_dir])

def test_install_dependencies():
    env_dir = 'test_venv'
    requirements_file = 'test_requirements.txt'
    with open(requirements_file, 'w') as f:
        f.write('requests\n')
    setup_initialization.create_virtualenv(env_dir)
    setup_initialization.install_dependencies(env_dir, requirements_file)
    # Check if pip installed requests in the virtualenv
    pip_freeze = subprocess.check_output([os.path.join(env_dir, 'bin', 'pip'), 'freeze']).decode()
    assert 'requests' in pip_freeze
    # Clean up
    subprocess.call(['rm', '-rf', env_dir])
    os.remove(requirements_file)
