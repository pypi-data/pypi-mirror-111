from setuptools import setup

setup(name='sylo',
      version='0.2',
      description='SYLO Python Pomodoro Timer',
      url='http://github.com/rob-parker-what/sylo',
      author='Rob Parker',
      author_email='robparkerwhat.dev@gmail.com',
      license='MIT',
      packages=['sylo'],
      entry_points={
          'console_scripts': ['sylo=sylo.cmdline:main'],
      },
      zip_safe=False)
