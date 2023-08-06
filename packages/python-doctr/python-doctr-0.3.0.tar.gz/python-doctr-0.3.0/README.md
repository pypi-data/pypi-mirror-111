
# DocTR: Document Text Recognition

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE) ![Build Status](https://github.com/mindee/doctr/workflows/builds/badge.svg) [![codecov](https://codecov.io/gh/mindee/doctr/branch/main/graph/badge.svg?token=577MO567NM)](https://codecov.io/gh/mindee/doctr) [![CodeFactor](https://www.codefactor.io/repository/github/mindee/doctr/badge?s=bae07db86bb079ce9d6542315b8c6e70fa708a7e)](https://www.codefactor.io/repository/github/mindee/doctr) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/340a76749b634586a498e1c0ab998f08)](https://app.codacy.com/gh/mindee/doctr?utm_source=github.com&utm_medium=referral&utm_content=mindee/doctr&utm_campaign=Badge_Grade) [![Doc Status](https://github.com/mindee/doctr/workflows/doc-status/badge.svg)](https://mindee.github.io/doctr) [![Pypi](https://img.shields.io/badge/pypi-v0.2.1-blue.svg)](https://pypi.org/project/python-doctr/) 


**Optical Character Recognition made seamless & accessible to anyone, powered by TensorFlow 2 (PyTorch in beta)**


What you can expect from this repository:
- efficient ways to parse textual information (localize and identify each word) from your documents
- guidance on how to integrate this in your current architecture

![OCR_example](https://github.com/mindee/doctr/releases/download/v0.2.0/ocr.png)

## Quick Tour

### Getting your pretrained model

End-to-End OCR is achieved in DocTR using a two-stage approach: text detection (localizing words), then text recognition (identify all characters in the word).
As such, you can select the architecture used for [text detection](https://mindee.github.io/doctr/latest/models.html#id2), and the one for [text recognition](https://mindee.github.io/doctr/latest/models.html#id3) from the list of available implementations.

```python
from doctr.models import ocr_predictor

model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
```

### Reading files

Documents can be interpreted from PDF or images:

```python
from doctr.documents import DocumentFile
# PDF
pdf_doc = DocumentFile.from_pdf("path/to/your/doc.pdf").as_images()
# Image
single_img_doc = DocumentFile.from_images("path/to/your/img.jpg")
# Webpage
webpage_doc = DocumentFile.from_url("https://www.yoursite.com").as_images()
# Multiple page images
multi_img_doc = DocumentFile.from_images(["path/to/page1.jpg", "path/to/page2.jpg"])
```

### Putting it together
Let's use the default pretrained model for an example:
```python
from doctr.documents import DocumentFile
from doctr.models import ocr_predictor

model = ocr_predictor(pretrained=True)
# PDF
doc = DocumentFile.from_pdf("path/to/your/doc.pdf").as_images()
# Analyze
result = model(doc)
```

To make sense of your model's predictions, you can visualize them as follows:

```python
result.show(doc)
```

![DocTR example](https://github.com/mindee/doctr/releases/download/v0.1.1/doctr_example_script.gif)

or export them to JSON format (to get a better understanding of our document model, check our [documentation](https://mindee.github.io/doctr/documents.html#document-structure)):

```python
json_output = result.export()
```


## Installation

Python 3.6 (or higher) and [pip](https://pip.pypa.io/en/stable/) are required to install DocTR. Additionally, you will need to install at least one of [TensorFlow](https://www.tensorflow.org/install/) or [PyTorch](https://pytorch.org/get-started/locally/#start-locally).

You can then install the latest release of the package using [pypi](https://pypi.org/project/python-doctr/) as follows:

```shell
pip install python-doctr
```

Or you can install it from source:

```shell
git clone https://github.com/mindee/doctr.git
pip install -e doctr/.
```

Since we use [weasyprint](https://weasyprint.readthedocs.io/), you will need extra dependencies if you are not running Linux.
For MacOS users, you can install them as follows:
```shell
brew install cairo pango gdk-pixbuf libffi
```

For Windows users, those dependencies are included in GTK. You can find the latest installer over [here](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases).


## Models architectures
Credits where it's due: this repository is implementing, among others, architectures from published research papers.

### Text Detection
- [Real-time Scene Text Detection with Differentiable Binarization](https://arxiv.org/pdf/1911.08947.pdf).
- [LinkNet: Exploiting Encoder Representations forEfficient Semantic Segmentation](https://arxiv.org/pdf/1707.03718.pdf)

### Text Recognition
- [An End-to-End Trainable Neural Network for Image-based Sequence Recognition and Its Application to Scene Text Recognition](https://arxiv.org/pdf/1507.05717.pdf).
- [Show, Attend and Read:A Simple and Strong Baseline for Irregular Text Recognition](https://arxiv.org/pdf/1811.00751.pdf).
- [MASTER: Multi-Aspect Non-local Network for Scene Text Recognition](https://arxiv.org/pdf/1910.02562.pdf).


## More goodies

### Documentation

The full package documentation is available [here](https://mindee.github.io/doctr/) for detailed specifications.


### Demo app

A minimal demo app is provided for you to play with the text detection model!

You will need an extra dependency ([Streamlit](https://streamlit.io/)) for the app to run:
```shell
pip install -r demo/requirements.txt
```
You can then easily run your app in your default browser by running:

```shell
streamlit run demo/app.py
```

![Demo app](https://github.com/mindee/doctr/releases/download/v0.2.1/demo.png)

### Docker container

If you are to deploy containerized environments, you can use the provided Dockerfile to build a docker image:

```shell
docker build . -t <YOUR_IMAGE_TAG>
```

### Example script

An example script is provided for a simple documentation analysis of a PDF or image file:

```shell
python scripts/analyze.py path/to/your/doc.pdf
```
All script arguments can be checked using `python scripts/analyze.py --help`


### Minimal API integration

Looking to integrate DocTR into your API? Here is a template to get you started with a fully working API using the wonderful [FastAPI](https://github.com/tiangolo/fastapi) framework.

#### Deploy your API locally
Specific dependencies are required to run the API template, which you can install as follows:
```shell
pip install -r api/requirements.txt
```
You can now run your API locally:

```shell
uvicorn --reload --workers 1 --host 0.0.0.0 --port=8002 --app-dir api/ app.main:app
```

Alternatively, you can run the same server on a docker container if you prefer using:
```shell
PORT=8002 docker-compose up -d --build
```

#### What you have deployed

Your API should now be running locally on your port 8002. Access your automatically-built documentation at [http://localhost:8002/redoc](http://localhost:8002/redoc) and enjoy your three functional routes ("/detection", "/recognition", "/ocr"). Here is an example with Python to send a request to the OCR route:

```python

import requests
import io
with open('/path/to/your/doc.jpg', 'rb') as f:
    data = f.read()
response = requests.post("http://localhost:8002/ocr", files={'file': io.BytesIO(data)}).json()
```


## Citation

If you wish to cite this project, feel free to use this [BibTeX](http://www.bibtex.org/) reference:

```bibtex
@misc{doctr2021,
    title={DocTR: Document Text Recognition},
    author={François-Guillaume Fernandez, Charles Gaillard},
    year={2021},
    publisher = {GitHub},
    howpublished = {\url{https://github.com/mindee/doctr}}
}
```


## Contributing

If you scrolled down to this section, you most likely appreciate open source. Do you feel like extending the range of our supported characters? Or perhaps submitting a paper implementation? Or contributing in any other way?

You're in luck, we compiled a short guide (cf. [`CONTRIBUTING`](CONTRIBUTING.md)) for you to easily do so!


## License

Distributed under the Apache 2.0 License. See [`LICENSE`](LICENSE) for more information.

