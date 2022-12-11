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
RUN pip install -r requirements.txt

CMD [ "python", "main.py"]