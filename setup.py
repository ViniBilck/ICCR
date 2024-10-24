from setuptools import setup, find_packages

setup(
    name='ICCR',
    version='0.1',
    python_requires='>=3.7',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'make_collision=iccr:Collision',  # Adjust path if necessary
            'make_orbit=iccr:Collision',          # Add similar lines for other scripts
            'get_ids_range=iccr:Collision',
            'make_rotation=iccr:Collision',
            'get_masses=iccr:Collision',
        ],
    },
    description="Initial Condition to Collision Route",
    author="Vinicius Lourival Bilck",
    author_email="bilck.vinicius1998@gmail.com",
    url='https://github.com/ViniBilck/ICCR',
    platforms=['Linux'],
    license="MIT License",
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
    ],
)

