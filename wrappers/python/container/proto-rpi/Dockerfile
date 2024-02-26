# build protobuff wheel
FROM wirepas/base:1.0-raspbian as wm-proto-builder
RUN [ "cross-build-start" ]
USER root
ARG GIT_TAG=${GIT_TAG:-"v3.7.1"}
RUN sudo apt-get update \
    && sudo apt-get install autoconf automake libtool curl make g++ unzip git

WORKDIR /app_build
RUN git clone https://github.com/protocolbuffers/protobuf.git \
    && cd protobuf \
    && git checkout ${GIT_TAG}\
    && git submodule update --init --recursive \
    && ./autogen.sh \
    && ./configure \
    && make \
    && make check \
    && sudo make install \
    && sudo ldconfig

#configure --disable-shared\

WORKDIR /app_build/protobuf/python/
RUN python3 setup.py build --cpp_implementation \
    && python3 setup.py test --cpp_implementation \

RUN [ "cross-build-end" ]
