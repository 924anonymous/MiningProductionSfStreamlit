FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

RUN git clone https://github.com/924anonymous/MiningProductionSfStreamlit.git .

RUN pip install -r requirements.txt

EXPOSE 8502

ENTRYPOINT ["streamlit", "run", "MainUiApp.py", "--server.port=8502", "--server.address=0.0.0.0"]