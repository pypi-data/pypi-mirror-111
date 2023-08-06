import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="jsonrpcx",
    version="3.0.0",
    description="A battle tested Python JSON-RPC2.0 library supporting client and server code in sync and async fashion.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeberg.org/_laphilipa/jsonrpcx",
    packages=setuptools.find_packages(),
    # anyio is required for async parts in httpx
    install_requires=['httpx', 'anyio', 'pytz', 'tzlocal'],
    license="ISC",
    keywords = ['JSON', 'jsonrpc', 'rpc'],
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Internet",
        "Topic :: Home Automation",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
)
