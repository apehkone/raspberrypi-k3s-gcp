FROM balenalib/raspberrypi4-64-debian-python:3.7.3-stretch-build as build

WORKDIR /app
# Sets utf-8 encoding for Python
ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Make sure we use the virtualenv:
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Use `install_packages` if you need to install dependencies
RUN pip install -U pip && \
    pip install --upgrade pip && \
    pip install -U wheel && \
    pip install -U numpy && \
    pip install -U pillow

# RTIMU library fix
RUN git clone https://github.com/RPi-Distro/RTIMULib/ RTIMU
WORKDIR /app/RTIMU/Linux/python

RUN python setup.py build && \
    python setup.py install

# reset working directory
WORKDIR /app

COPY ./src/requirements.txt ./
RUN pip install -U --no-cache-dir -r requirements.txt

# Trimmed down app container
FROM balenalib/raspberrypi4-64-debian-python:3.7.3-stretch-build as app
# Extra python env
ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UDEV=1 
# Use `install_packages` if you need to install dependencies
RUN install_packages libjpeg62-turbo-dev

# Copy build artifacts from the previous stage into this new stage
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Always set a working directory
WORKDIR /app
COPY ./src /app

# main.py will run when container starts up on the device
CMD ["python", "-u", "app.py"]
