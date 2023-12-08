FROM python:latest
ADD HZZAnalysis/Outputter/outputter.py HZZAnalysis/Outputter/outputter_functions.py HZZAnalysis/samples.json HZZAnalysis/constants.py ./
RUN pip install --upgrade pika awkward numpy matplotlib
CMD [ "python", "./outputter.py"]