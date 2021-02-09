FROM openjdk:8-jdk-slim-buster

ENV REPRO_NAME  timeseries-service
ENV REPRO_MNT   /mnt/${REPRO_NAME}
ENV REPRO_USER  repro
ENV REPRO_UID   1000
ENV REPRO_GID   1000

RUN echo '***** Update package index *****'                                 \
 && apt -y update

RUN echo '***** Install packages required for creating this image *****'    \
 && apt -y install apt-utils wget curl makepasswd                           \
                                                                            \
 &&  echo '***** Install command-line utility packages *****'               \
 && apt -y install git sudo less file tree make procps

 RUN echo '***** Install python3, pip3, and numpy *****'                    \
 && apt -y install python3 python3-pip                                      \
 && pip3 install --upgrade pip                                              \
 && pip3 install numpy                                                      \
 && cd /usr/bin && ln -s python3 python

RUN apt -y install pkg-config sqlite3 libsqlite3-dev libtiff-dev

RUN echo '***** download source packages for PROJ *****'                    \
 && mkdir -p /tmp/builds                                                    \
 && cd /tmp/builds                                                          \
 && wget https://download.osgeo.org/proj/proj-7.2.1.tar.gz                  \
 && gunzip proj-7.2.1.tar.gz                                                \
 && tar -xvvf proj-7.2.1.tar                                                \
 && cd ./proj-7.2.1                                                         \
 && ./configure --without-curl                                              \
 && make                                                                    \
 && make install                                                            \
 && ldconfig                                                                \
 && cd /tmp/builds                                                          \
 && rm -rf proj-7.2*

RUN echo '***** download source package for GDAL *****'                     \
 && mkdir -p /tmp/builds                                                    \
 && cd /tmp/builds                                                          \
 && wget https://github.com/OSGeo/gdal/releases/download/v3.2.1/gdal-3.2.1.tar.gz \
 && gunzip gdal-3.2.1.tar.gz                                                \
 && tar -xvvf gdal-3.2.1.tar                                                \
                                                                            \
 && echo '***** configure and build GDAL with Python3 bindings ******'      \
 && cd /tmp/builds/gdal-3.2.1                                               \
 && mkdir -p /opt/gdal                                                      \
 && ./configure --prefix /opt/gdal/gdal-3.2.1                               \
                --with-python=$(which python3)                              \
 && make install                                                            \
 && cd /tmp/builds                                                          \
 && rm -rf gdal-3.2*

ENV LD_LIBRARY_PATH=/opt/gdal/gdal-3.2.1/lib/
ENV PYTHONPATH=/opt/gdal/gdal-3.2.1/lib/python3/dist-packages/
ENV PATH=/opt/gdal/gdal-3.2.1/bin/:$PATH

RUN echo '***** Download and install maven *****'                           \
 && MAVEN_REPO=https://mirrors.gigenet.com/apache/maven/maven-3             \
 && MAVEN_VERSION=3.6.3                                                     \
 && MAVEN_RELEASE_DIR=${MAVEN_REPO}/${MAVEN_VERSION}/binaries               \
 && MAVEN_RELEASE_NAME=apache-maven-${MAVEN_VERSION}                        \
 && MAVEN_ARCHIVE=${MAVEN_RELEASE_NAME}-bin.tar.gz                          \
 && MAVEN_BIN_DIR=/opt/${MAVEN_RELEASE_NAME}/bin                            \
 && cd /opt                                                                 \
 && wget -O ${MAVEN_ARCHIVE} ${MAVEN_RELEASE_DIR}/${MAVEN_ARCHIVE}          \
 && tar -xvf ${MAVEN_ARCHIVE}                                               \
 && mv ${MAVEN_RELEASE_NAME} maven-3                                        \
 && rm ${MAVEN_ARCHIVE}

COPY service /mnt/timeseries-service/service
COPY data /mnt/timeseries-service/data

RUN echo '***** Make service directory accesible *****' \
    && chown -R ${REPRO_UID}.${REPRO_GID} ${REPRO_MNT}/service

RUN echo '***** Download and install Node.js from NodeSource *****'         \
    && curl -sL https://deb.nodesource.com/setup_15.x | bash -              \
    && apt install -y nodejs

RUN echo '***** Ensure default python version is 3 *****'                   \
    && cd /usr/bin && rm -f python && ln -s python3 python

RUN echo '***** Add the REPRO user and group *****'                         \
    && groupadd ${REPRO_USER} --gid ${REPRO_GID}                            \
    && useradd ${REPRO_USER} --uid ${REPRO_UID} --gid ${REPRO_GID}          \
        --shell /bin/bash                                                   \
        --create-home                                                       \
        -p `echo repro | makepasswd --crypt-md5 --clearfrom - | cut -b8-`   \
    && echo "${REPRO_USER} ALL=(ALL) NOPASSWD: ALL"                         \
            > /etc/sudoers.d/${REPRO_USER}                                  \
    && chmod 0440 /etc/sudoers.d/repro

ENV HOME /home/${REPRO_USER}
ENV BASHRC ${HOME}/.bashrc
USER  ${REPRO_USER}
WORKDIR $HOME

COPY java/maven-settings.xml ${HOME}/.m2/settings.xml

ENV PATH ${HOME}/.local/bin:${PATH}
ENV PYTHON_SCRIPTS_DIR ${HOME}/python

COPY python ${PYTHON_SCRIPTS_DIR}

RUN echo '***** Install the Python scripts *****'    \
 && cd ${PYTHON_SCRIPTS_DIR}                         \
 && pip3 install .

ENV PATH /opt/maven-3/bin:$PATH

RUN echo "export PATH=${PATH}" >> ${BASHRC}
RUN echo "export IN_RUNNING_REPRO=${REPRO_NAME}" >> ${BASHRC}
RUN echo "cd ${REPRO_MNT}" >> ${BASHRC}

CMD  /bin/bash -il
