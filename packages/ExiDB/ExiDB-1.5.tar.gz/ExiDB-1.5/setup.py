from setuptools import setup,find_packages


setup(
   name='ExiDB',
   version='1.5',
   description='ExiDB it is an easier way to make a simple database with simple Query',
   license="MIT",
   long_description=open('README.md','r').read(),
   long_description_content_type='text/x-rst',
   author='Zaid Ali',
   author_email='email@iexi.xyz',
   keywords=['db','database','json'],
    packages=['exidb'],
    install_requires=["jsonpath"],
    package_dir={'exidb': 'exidb'},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)