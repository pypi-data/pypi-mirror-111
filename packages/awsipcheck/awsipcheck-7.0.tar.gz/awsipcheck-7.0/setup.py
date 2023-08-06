import setuptools
import subprocess
import os

# awsipcheck_version = (
#     subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
#     .stdout.decode("utf-8")
#     .strip()
# )
# assert "." in awsipcheck_version

# assert os.path.isfile("awsipcheck/version.py")
# with open("awsipcheck/VERSION", "w", encoding="utf-8") as fh:
#     fh.write(f"{awsipcheck_version}\n")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    
def main():
    import awsipcheck as app
    setuptools.setup(
        name="awsipcheck",
        version=app.__version__,
        author="Amal Murali",
        author_email="amalmurali47@gmail.com",
        description="Sample tool",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/amalmurali47/awsipcheck",
        packages=setuptools.find_packages(),
        package_data={"awsipcheck": ["VERSION"]},
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
        entry_points={"console_scripts": ["awsipcheck = awsipcheck:__main__.main"]},
        install_requires=[
            "requests >= 2.25.1",
            "pytricia >= 1.0.2"
        ],
    )
    
if __name__ == '__main__':
    main()
