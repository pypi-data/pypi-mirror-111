from setuptools import setup, find_packages
setup(name="age-finder", 
      version="0.0.1",
      author="chrisp",
      author_email="christopherpearce10@gmail.com",
      long_description=open("README.md").read(),
      install_requires=["wheel", "selenium"],
      packages=find_packages(where='.', include='*'),
      include_package_data=True)