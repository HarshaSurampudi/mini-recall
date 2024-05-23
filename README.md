# mini-recall

A small and simple attempt to implement the Microsoft's new [Recall](https://learn.microsoft.com/en-us/windows/ai/apis/recall) feature.

This application has four main components:

- A python service that takes a screenshot of the PC every few seconds and stores in a folder.
- A python service that processes the screenshots by fetching the image embeddings and storing them in a vector database - [qdrant](https://qdrant.tech/)
- A FastAPI api that serves endpoints to query the vector database and fetch the most related images for a given text query.
- A simple frontend that talks to the api for querying the images using text and displays the results.

This project uses the [CLIP-ViT-g-14](https://huggingface.co/laion/CLIP-ViT-g-14-laion2B-s12B-b42K) model and [open_clip](https://github.com/mlfoundations/open_clip) for image and text embeddings. Check [server.py](server.py) to see how the embeddings are generated.

The results are not perfect and the model is not fine-tuned. The main goal of this project is to understand the working of the Recall feature and to build a simple prototype. As the type of images are all screenshots from a computer, the results are not very accurate. But are considerably good. The model can be fine-tuned on a dataset of screenshots to improve the results.

🚧 This project is a work in progress and is not yet complete.

## Installation

### Python Services

Creating a virtual environment is recommended.

```bash
git clone
cd mini-recall
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

### Qdrant

Follow the instructions in the [qdrant](https://qdrant.tech/documentation/quick-start/) documentation to setup qdrant.

## Usage

### Python Services

```bash
python capture_service.py
python processing_service.py
python server.py
```

### Frontend

```bash
cd frontend
npm start
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
