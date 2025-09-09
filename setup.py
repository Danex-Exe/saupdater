from setuptools import setup, find_packages

setup(
    name="saupdater",
    description='Updating a project when a version changes',
    long_description='The module checks for the presence of a .version file in the local repository, as well as the presence of a remote git source. It then compares the contents of the .version file on the repository and the local one. If there are differences, it executes the git pull command.',
    author='Daniil Alekseev',
    author_email='sevenaspects.mail@gmail.com',
    version="1.0.1",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.8",
)
