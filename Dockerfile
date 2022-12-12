FROM nvcr.io/nvidia/pytorch:22.11-py3


ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
    libsndfile1 sox \
    libfreetype6 \
    swig \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir app
RUN cd app
WORKDIR /app/
COPY ./api/app ./app/
COPY .env .
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/openai/whisper.git 
RUN pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
RUN pip install setuptools-rust


CMD [ "python", "main.py"]