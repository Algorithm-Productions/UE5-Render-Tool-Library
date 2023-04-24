import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="algorithm-ue5-lib",
    version="0.0.1",
    author="Algorithm Productions.ie",
    description="Utility Library for Algorithm's Render Farm Software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    py_modules=["algorithm-ue5-lib"],
    package_dir={'': 'algorithm-ue5-lib/src'},
    install_requires=[
        "logging",
        "requests",
        "datetime",
        "os",
        "platform",
        "uuid",
        "flask",
        "statistics",
        "time",
        "GPUtil"
        "psutil",
        "subprocess",
        "threading",
        "abc",
        "json",
        "socket"
    ]
)
