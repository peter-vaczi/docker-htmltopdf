FROM ubuntu:18.04

RUN apt update && \
    apt install -y \
        curl \
        fontconfig \
        libfontconfig1 \
        libfreetype6 \
        fontconfig-config \
        ucf \
        fonts-dejavu-core \
        ttf-bitstream-vera \
        fonts-liberation \
        libexpat1 \
        libpng16-16 \
        libjpeg-turbo8 \
        libx11-6 \
        libxcb1 \
        libx11-data \
        libxau6 \
        libxdmcp6 \
        libbsd0 \
        multiarch-support \
        libxext6 \
        libxrender1 \
        xfonts-75dpi \
        xfonts-base \
        xfonts-utils \
        libfontenc1 \
        x11-common \
        xfonts-encodings && \
    curl -LSsO https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb && \
    dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb && \
    rm wkhtmltox_0.12.5-1.bionic_amd64.deb && \
    apt remove -y curl && \
    apt autoremove -y

RUN apt-get install -y python-pip
RUN pip install flask executor

COPY app.py /app.py
EXPOSE 80

ENV FLASK_APP app.py

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
