from setuptools import setup
with open("README.md", "r", encoding="utf-8") as f:
    LongDescription = f.read()
setup(
    name = "schedules",
    packages = ["schedules"],
    version = "1.2",
    license = "MIT",
    description = "Create non-blocking scheduled tasks.",
    long_description = LongDescription,
    long_description_content_type = "text/markdown",
    author = "YishaiYosifov",
    author_email = "yishai247@gmail.com",
    url = "https://github.com/YishaiYosifov/schedules",
    keywords = ["schedule", "task", 'nonblocking', "scheduler", "non-blocking", "schedules"],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
  ],
)