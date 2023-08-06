from setuptools import setup

setup(
    name='galacticatipsy', # pip install name i.e. would be pip install Boris-Ext
    version='0.0.5', # THis is very important of it will not upload. SO IT MUST CHANGE ON EVERY UPDATE
    description='Package for Galactica Tipsy',
    url='http://www.star.uclan.ac.uk/~sgough-kelly/galactica/',
    author='Steven Gough-Kelly',
    author_email='steventgk@gmail.com',
    license='LGPL',
    packages=['galacticatipsy'], # Package name holding .py files. File holding NetSocks.py and shaper.py
    install_requires=['numpy','matplotlib'
                      ], #What needs to be installed for you module. If you use any external modules like pandas in your library add it here.

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',

    ],
)
