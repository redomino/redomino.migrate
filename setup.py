from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='redomino.migrate',
      version=version,
      description="Plone migration utilities",
      long_description=""" This product contains utilities to help migration from older versions of Plone. """,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Plone migration',
      author='Fabrizio Reale',
      author_email='fabrizio.reale@redomino.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['redomino'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.jsonmigrator'
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
