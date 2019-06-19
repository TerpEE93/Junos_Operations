from setuptools import setup, find_packages

import junos_common_operations.about as about


def requirements(filename='requirements.txt'):
  return open(filename.strip()).readlines()


with open("README.md", "r") as fh:
  long_description = fh.read()

with open("LICENSE.md", "r") as fh:
  license_file = fh.read()


setup(
    name=about.package_name,
    version=about.package_version,
    description='Juniper Operations Tools',
    license=license_file,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Juniper Networks',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=requirements(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        fabric_op=junos_common_operations.op_tools:main
    '''
)
