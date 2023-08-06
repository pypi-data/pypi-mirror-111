import setuptools

with open("README.md", 'r', encoding="utf-8") as fin:
    long_desc = fin.read()

reqs = [
    "jinja2",
    "pygments",
    "flask",
    "flask_cas",
    "importlib_resources",
    "pytest"
]

setuptools.setup(
    name="potluck-eval",
    version="0.7.2",
    requires=reqs,
    extras_require={ 'tests': reqs }, # for tox, for some silly reason
    python_requires=">=3.6", # f-strings are used
    provides=["potluck", "potluck_server"],
    url="https://cs.wellesley.edu/~pmwh/potluck/docs/",
    description=(
        "Python code evaluation system and submissions server capable"
        " of unit tests, tracing, and AST inspection."
    ),
    author="Peter Mawhorter",
    author_email="pmawhort@wellesley.edu",
    packages=["potluck", "potluck.tests", "potluck_server"],
    include_package_data=True, # include data in packages that's in MANIFEST.in
    scripts=["scripts/potluck_eval"],
    # Note: MANIFEST.in handles package data
    license="BSD 3-Clause License",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: Flask",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Education",
    ],
    long_description=long_desc,
    long_description_content_type="text/markdown"
)
