from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'bog_yz5'

setup(
    name=package_name,
    version='0.0.2',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*launch.[pxy][yma]*')), 
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bog_yz5',
    maintainer_email='bogjos.kevin@gmail.com',
    description='Autonóm Vészfék szimuláció és vezérlő - kis beadandó az AJR tantárgyhoz',
    license='GNU General Public License v3.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gen_range_twist = bog_yz5.gen_range_twist:main',
            'control_node = bog_yz5.control_node:main',
        ],
    },
)
