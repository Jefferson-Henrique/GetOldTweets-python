import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    INSTALL_REQUIRES = [l.split('#')[0].strip() for l in fh if not l.strip().startswith('#')]

setuptools.setup(
    name="GetOldTweets3",
    version="0.0.5",
    author="Dmitry Mottl",
    author_email="dmitry.mottl@gmail.com",
    license='MIT',
    description="Get old tweets from Twitter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mottl/GetOldTweets3",
    keywords="twitter tweets",
    packages=setuptools.find_packages(),
    scripts=['bin/GetOldTweets3'],
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
    ],
    python_requires='>=3.4',
    install_requires=INSTALL_REQUIRES
)
