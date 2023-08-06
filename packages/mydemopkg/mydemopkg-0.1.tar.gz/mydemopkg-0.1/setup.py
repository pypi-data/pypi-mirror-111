from setuptools import setup

setup(name='mydemopkg',
      version='v0.1',
      author="Madhura Ganguly",
      author_email='gangulym23@gmail.com',
      description="Printing text",
      packages=['mydemopkg'],
      license='MIT',
      url="https://github.com/gangulymadhura/mydemopkg",
      download_url='https://github.com/gangulymadhura/mydemopkg/archive/refs/tags/v0.1.tar.gz',
      install_requires=[],
      tests_require=['unittest'],
      test_suite='tests',
      python_requires='>=3.5',
      zip_safe=False)


# python setup.py sdist
# python -m twine upload --repository testpypi dist/*
# pip install -i https://test.pypi.org/simple/ discover_timeseries
# pip uninstall discover_timeseries
# python -m twine upload --repository pypi dist/*
# twine upload --skip-existing dist/*
