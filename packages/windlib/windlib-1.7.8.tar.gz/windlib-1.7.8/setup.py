try:
    from setuptools import setup
except:
    from distutils.core import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="windlib",
    version="1.7.8",
    author="SNWCreations",
    author_email="snwcreations@qq.com",
    description="A useful functions library for everyone.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/SNWCreations/windlib",
    packages=['windlib'],
    project_urls={
        "Bug Tracker": "https://gitee.com/SNWCreations/windlib/issues",
    },
    requries=[
        'contextlib',
        'gzip',
        'tarfile',
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Topic :: Software Development :: Libraries",
    ],
)
