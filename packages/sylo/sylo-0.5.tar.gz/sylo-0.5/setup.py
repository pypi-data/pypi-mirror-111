from setuptools import setup

setup(name='sylo',
      version='0.5',
      description='SYLO Python Pomodoro Timer',
      url='http://github.com/rob-parker-what/sylo',
      author='Rob Parker',
      author_email='robparkerwhat.dev@gmail.com',
      license='MIT',
      packages=['sylo'],
      entry_points={
          'console_scripts': ['sylo=sylo.cmdline:main'],
      },
      install_requires=[
            'colorama==0.4.4',
            'simpleaudio==1.0.4',
            'beepy==1.0.7',
      ],
      package_data={'sylo': ['audio/*.wav']},
      zip_safe=False)
