from setuptools import setup

setup(name = 'bmkg_data',
    author = 'Josef Matondang',
    author_email = 'admin@josefmtd.com',
    version = '0.1.0',
    description = 'BMKG Data Python Wrapper',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    keywords = 'earthquake',
    url = 'https://github.com/josefmtd/gee-fwi',
    license = 'MIT',
    packages = ['bmkg_data'],
    install_requires = [
        'pandas',
    ],
    include_package_data = True,
    zip_safe = False)
