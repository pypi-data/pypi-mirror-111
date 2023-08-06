from setuptools import setup

setup(
    name='example0934',
    version='0.1.0',    
    description='A example Python package',
    url="https://github.com/cobrobrown/dslab/pip package/example0934",
    author='Conner Brown',
    author_email='cobrobrown@gmail.com',
    license='BSD 2-clause',
    packages=['example0934'],
    install_requires=['numpy'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
    ],
)