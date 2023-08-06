from setuptools import setup, find_packages


setup(
    name='testlib3add',
    version=1235,
    license='MIT',
    author="Author Name",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://duckduckgo.com',
    keywords='example project',
    install_requires=[
          'numpy',
      ],

)
