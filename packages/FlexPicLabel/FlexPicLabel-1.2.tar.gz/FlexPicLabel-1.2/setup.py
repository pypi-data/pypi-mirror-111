from distutils.core import setup
setup(
  name = 'FlexPicLabel',         # How you named your package folder (MyLib)
  packages = ['FlexPicLabel'],   # Chose the same as "name"
  version = '1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'picture/video widget for pyside6/pyqt6',   # Give a short description about your library
  author = 'poshl9k',                   # Type in your name
  author_email = 'poshl9k@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/poshl9k/flexpiclabel',   # Provide either the link to your github or to your website
  keywords = ['pyside6', 'pyqt6', 'picture', 'video', 'widget'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'PySide6',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Widget Sets',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
  ],
)