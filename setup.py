from numpy.distutils.core import setup

package_data = {
    'ICCR': [
        'iccr/*',
    ]
}

setup(
    name='ICCR',
    python_requires='>=3.7',
    version="0.1",
    packages=['iccr'],
    package_data=package_data,
    scripts=['bin/make_collision', 'bin/make_orbit', 'bin/get_ids_range', 'bin/make_rotation', 'bin/get_masses'],
    description="Initial Condition to Collision Route",
    author="Vinicius Lourival Bilck",
    author_email="bilck.vinicius1998@gmail.com",
    url='https://github.com/ViniBilck/ICCR',
    platform='Linux',
    license="MIT License",
    classifiers=['Programming Language :: Python :: 3.7'],
)
