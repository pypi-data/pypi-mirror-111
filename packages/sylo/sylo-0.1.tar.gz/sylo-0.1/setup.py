from setuptools import setup

setup(name='sylo',
      version='0.1',
      description='SYLO Python Pomodoro Timer',
      url='http://github.com/rob-parker-what/sylo',
      author='Rob Parker',
      author_email='robparkerwhat.dev@gmail.com',
      license='MIT',
      packages=['sylo'],
      install_requires=[  # I get to this in a second
            'colorama',
            'simpleaudio',
            'beepy',
      ],
      zip_safe=False)
