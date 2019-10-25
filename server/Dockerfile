FROM continuumio/miniconda

# Copy source
COPY . content

# install basics
RUN apt-get update -y \
 && apt-get install -y libc-dev gcc

ENV PATH=/opt/conda/bin:$PATH

# Create a Python 3.7 environment
RUN conda install -y conda-build \
 && conda env create --file content/environment.yml \
 && conda clean -ya

ENV CONDA_DEFAULT_ENV=ml-web-demo
ENV CONDA_PREFIX=/opt/conda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-9

RUN sed -i '1 ! s/_gdbm/dbm/' $CONDA_PREFIX/lib/python3.7/dbm/gnu.py

WORKDIR /content

CMD python app.py
