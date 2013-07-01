try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.1'

setup(name='salesforce-api-client',
      version=VERSION,
      author='David Crawford',
      author_email='david@metricadb.com',
      url='https://github.com/davidcrawford/salesforce-api-client',
      description='Python client for using the Salesforce API',
      license='MIT',
      packages=['salesforce'],
      )
