import os

from glob import glob
from setuptools import find_packages, setup

package_name = 'dasrobot_voice'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),

    data_files=[
        ('share/ament_index/resource_index/packages',['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools', 'pyttsx3', 'SpeechRecognition'],
    zip_safe=True,

    maintainer='Dmitry Savin',
    maintainer_email='das.dev.dt@gmail.com',
    description='Voice processing package for the DASRobot',
    license='Apache-2.0',

    entry_points={
        'console_scripts': [
            'dasrobot_tts = dasrobot_voice.dasrobot_text_to_speech_node:main',
            'dasrobot_stt = dasrobot_voice.dasrobot_speech_to_text_node:main',
        ],
    },
)