import setuptools

with open('readme.md', 'r') as fh:
    long_description = fh.read()

    setuptools.setup(
        name='dymka',
        version='1.1.1',
        author='Denis Glotov',
        description='Swiss-knife cli for Ethereum-based blockchains',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/denisglotov/dymka',
        packages=setuptools.find_packages(),
        install_requires=[
            'web3',
        ],
        scripts=['dymka'],
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
        python_requires='>=3.6',
    )
