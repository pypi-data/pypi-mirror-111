
from distutils.core import setup
setup(
  name = 'tellter',         # How you named your package folder (MyLib)
  packages = ['tellter'],   # Chose the same as "name"
  version = '0.0.16',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A library that connects to the Tellter API',   # Give a short description about your library
  author = 'Nathan Lourenco',                   # Type in your name
  author_email = 'nathan@tellter.com',      # Type in your E-Mail
  url = 'https://github.com/CastelRune/tellter',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/CastelRune/tellter/archive/v_0013.tar.gz',    # I explain this later on
  keywords = ['bad word censoring'],
  install_requires=[
          'validators',
          'beautifulsoup4',
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
