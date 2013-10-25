from setuptools import setup, find_packages

setup(name = 'django_notification_framework',
      description = 'A notification framework for Django.',
      version = '1.0',
      author = 'Espen A. Kristiansen',
      packages=find_packages(exclude=['ez_setup']),
      install_requires = [
          'Django',
          'django-simple-rest',
      ],
      include_package_data=True,
      long_description = '',
      zip_safe=False
)
