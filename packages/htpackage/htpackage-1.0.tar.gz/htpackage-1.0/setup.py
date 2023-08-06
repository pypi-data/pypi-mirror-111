from setuptools import setup

setup(name='htpackage',
      version='1.0',
      description='Package with modifications of Hough transform',
      packages=['htpackage'],
      install_requires=["matplotlib",
                        "numpy",
                        "sklearn",
                        "opencv-python"],
      author_email='michadas5@gmail.com',
      zip_safe=False)
