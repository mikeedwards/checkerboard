'''
Created on Jan 10, 2012

@author: Mike_Edwards
'''
from distutils.core import setup

setup(name='checkerboard',
      version='0.0.1',
      description='Geospatial education apps for informal learning institutions',
      long_description=open('README.rst').read(),
      author='Mike Edwards',
      author_email='mike@onearmedman.copm',
      url='http://github.com/mikeedwards/checkerboard/',
      license='BSD',
      packages=['checkerboard', 
                'checkerboard.api',
                'checkerboard.community',
                'checkerboard.lib',
                'checkerboard.lib.poster',
                'checkerboard.spotter',
                'checkerboard.widgets',
                'checkerboard.community.migrations',
                'checkerboard.lib',
                'checkerboard.lib.poster',
                'checkerboard.spotter.migrations',
                'checkerboard.widgets'],
      package_data={'checkerboard.api':['templates/api/*/*.html'],
                    'checkerboard.spotter':['templates/spotter/*.html','static/spotter/css/*.css','static/spotter/js/*.js'],
                    'checkerboard.widgets':['templates/widgets/*.html','static/widgets/css/*.css'],
                    'checkerboard':['templates/*.html','templates/*/*.html'],
                    },
      include_package_data=True,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Education',
      ]
     )