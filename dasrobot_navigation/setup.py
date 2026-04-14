import os

from glob import glob
from setuptools import find_packages, setup

package_name = 'dasrobot_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),

    data_files=[
        ('share/ament_index/resource_index/packages',['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,

    maintainer='D.A. Savin',
    maintainer_email='das.dev.dt@gmail.com',
    description='Navigation package for the DASRobot',
    license='Apache-2.0',

    entry_points={
        'console_scripts': [
        ],
    },
)
