# DataprepandAnalysis

The submission contains two folders corresponding to each parts. In the folder Part 1, has a subfolder data containing the ground truth for GTSDB and TT100K datasets. 
The two `class_stats.py` computes the class distribution for the GTSDB dataset and `read_annot_file.py`. The other folder Part 2 contains the program for computing 
computing the error metrics of the two models. The subfolder updated_json contains the ground and the predicted detections of the models stored in the form of a dictionary into a json file. 
Where the each entry corresponds to the frame containing the coordinates of all the detections. Here the class of the detection is ignored as we are only interested in 
detection accuracy and not the prediction accuracy. 

To run any of the codes, go to the corresponding directory and run the following command from the terminal,
```
$ python <filename>
```
