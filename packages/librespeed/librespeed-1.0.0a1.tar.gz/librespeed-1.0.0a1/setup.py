from setuptools import setup


version = "1.0.0a1"
url = "https://github.com/dopstar/librespeed"

if "a" in version:
    dev_status = "3 - Alpha"
elif "b" in version:
    dev_status = "4 - Beta"
else:
    dev_status = "5 - Production/Stable"


with open("README.md") as fd:
    long_description = fd.read()


requirements = [
    "requests",
]

testing_requirements = [
    "flask",
    "pytest",
    "pytest-cov",
    "wheel",
    "codecov",
    "coverage",
    "mock",
    "faker",
    "trustme",
    "black",
]

linting_requirements = [
    "flake8",
    "bandit"
    "flake8-isort",
    "flake8-quotes",
]


setup(
    name="librespeed",
    version=version,
    packages=["librespeed"],
    install_requires=requirements,
    tests_require=testing_requirements,
    extras_require={"testing": testing_requirements, "linting": linting_requirements},
    author="Mkhanyisi Madlavana",
    author_email="mmadlavana@gmail.com",
    url=url,
    project_urls={
        'Documentation': 'https://dopstar.github.io/librespeed',
        'Source': url,
        'Tracker': '{}/issues'.format(url),
    },
    download_url="{url}/archive/{version}.tar.gz".format(url=url, version=version),
    description=(
        "A Python client library for LibreSpeed"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=["LibreSpeed", "speedtest"],
    package_dir={"librespeed": "librespeed"},
    package_data={"librespeed": ["*.md", "LICENSE"]},
    classifiers=[
        "Development Status :: {0}".format(dev_status),
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
