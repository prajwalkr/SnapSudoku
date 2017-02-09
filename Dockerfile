FROM python:2-onbuild
LABEL repo "https://github.com/prajwalkr/SnapSudoku"
RUN apt-get update && apt-get install -y python-opencv
CMD [ "./test_training_images.sh" ]
