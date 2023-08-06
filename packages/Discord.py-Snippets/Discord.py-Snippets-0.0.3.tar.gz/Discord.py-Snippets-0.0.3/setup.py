from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Discord.py-Snippets',
  version='0.0.3',
  description='A package with discord.py snipets',
  long_description=open('README.md').read() + '\n\n' + open('CL.txt').read(),
  url='',  
  author='JustBetterL',
  author_email='palmspops@protonmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='discordsnips', 
  packages=find_packages(),
  install_requires=['discord.py'] 
)
