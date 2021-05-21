FROM continuumio/miniconda:latest

WORKDIR /home/docker_conda_template

COPY * ./

RUN chmod +x boot.sh

RUN conda env create -f environment.yml

RUN echo "source activate baseapi" > ~/.bashrc
ENV PATH /opt/conda/envs/baseapi/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["app.py"]
