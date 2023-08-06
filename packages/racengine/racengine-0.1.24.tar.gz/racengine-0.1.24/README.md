[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)]()
[![PyPI](https://img.shields.io/pypi/wheel/Django.svg)]()
# racapi-service

Take a docx template, json data and return PDF(default) or other format file

We can send the file by e-mail if we specifie a SMTPconf and a valid message object as described in demo.py file

Use [SFERENO's templater](https://hub.docker.com/r/sfereno/docxtemplater/) and [SFERENO's converter](https://hub.docker.com/r/sfereno/docker-libreoffice/) as endpoints

# Install using pip

You'll need to install wheel ```pip install wheel```

Create a Source Distribution:

```
python setup.py sdist
```

Create a wheel

```
python setup.py bdist_wheel
```

You can then install the package using pip
```cd dist && pip install package_name.whl```

# Getting started
See the demo.py file