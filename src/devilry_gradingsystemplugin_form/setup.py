from setuptools import setup, find_packages


setup(name = 'devilry_gradingsystemplugin_form',
      description = 'Devilry grading system plugin that requires examiners fill in a schema.',
      version = '1.0',
      license='BSD',
      author = 'Espen Angell Kristiansen',
      packages=find_packages(exclude=['ez_setup']),
      install_requires = [
          'setuptools',
          'django-crispy-forms',
      ],
      include_package_data=True,
      long_description = 'Grading system plugin.',
      zip_safe=False,
      classifiers=[
                   'Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python'
                  ]
)
