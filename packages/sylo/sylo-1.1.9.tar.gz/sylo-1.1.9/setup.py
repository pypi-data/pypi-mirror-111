from setuptools import setup


VERSION = "1.1.9"


with open("README.md") as f:
    readme = f.read()


setup(
    name="sylo",
    version=VERSION,
    description="SYLO Python Pomodoro Timer",
    long_description=readme,
    long_description_content_type="text/markdown",  # This is important!
    url="http://github.com/rob-parker-what/sylo",
    author="Rob Parker",
    author_email="robparkerwhat.dev@gmail.com",
    license="MIT",
    packages=["sylo"],
    entry_points={
        "console_scripts": ["sylo=sylo.cmdline:main"],
    },
    install_requires=[
        "colorama==0.4.4",
        "simpleaudio==1.0.4",
        "beepy==1.0.7",
    ],
    package_data={"sylo": ["audio/*.wav"]},
    zip_safe=False,
    python_requires='>=3',
    keywords="pomodoro tomato timer terminal pomodoro-timer",
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 "Programming Language :: Python",
                 'Topic :: Software Development',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'Operating System :: Unix',
                 'Operating System :: MacOS'],
)
