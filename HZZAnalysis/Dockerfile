# base on latest python image
FROM python:latest
ADD main.py infofile.py functions.py ./
RUN pip install numpy matplotlib uproot awkward vector
CMD [ "python", "./main.py"]