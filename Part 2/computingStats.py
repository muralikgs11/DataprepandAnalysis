#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:54:25 2019

@author: murali

Program computes the statistcs between GT and the predictions
Inputs: GT json file, corresponding prediction json file
"""
import json

def pred2GTindex(frame_id):
    return '{0:07}'.format(int(frame_id[:7]) + 1) + '.jpg'

def readJSON(path):
    with open(path, 'r') as myfile:
        data = myfile.read()
    
    data_dict = json.loads(data)
    return data_dict

def updateClusterDict(gt_frame, gt_dict, cluster_dict):
    
    for c_id in cluster_dict:
        cluster_dict[c_id]['change'] = 0
    
    for objects in gt_dict[gt_frame]:
        c_id = objects[4]
        try:
            cluster_dict[c_id]['coords'] = objects[:4]
            cluster_dict[c_id]['change'] = 1
        except:
            cluster_dict[c_id] = dict()
            cluster_dict[c_id]['coords'] = objects[:4]
            cluster_dict[c_id]['change'] = 1
            cluster_dict[c_id]['det'] = 0
            
    return cluster_dict

def final_updateCD(cluster_dict, stats_dict):
    rem_list = list()
    for cluster in cluster_dict:
        if cluster_dict[cluster]['change'] == 0:
            if cluster_dict[cluster]['det'] == 0:
                stats_dict['FN'] += 1
            else:
                stats_dict['TP'] += 1
            
            rem_list.append(cluster)
            
    for cluster in rem_list:
        cluster_dict.pop(cluster,None)
    return cluster_dict, stats_dict

def cvtCoords(c):
    return [c[0], c[1], c[0] + c[2], c[1] + c[3]]

def comArea(coords):
    width = coords[2] - coords[0]
    height = coords[3] - coords[1]
    area = 0
    if width > 0 and height > 0:
        area = width * height
    return area

def interCoords(d_coords, t_coords):
    x1 = (d_coords[0] > t_coords[0])*d_coords[0] + (d_coords[0] <= t_coords[0])*t_coords[0] 
    y1 = (d_coords[1] > t_coords[1])*d_coords[1] + (d_coords[1] <= t_coords[1])*t_coords[1]
    x2 = (d_coords[2] < t_coords[2])*d_coords[2] + (d_coords[2] >= t_coords[2])*t_coords[2]
    y2 = (d_coords[3] < t_coords[3])*d_coords[3] + (d_coords[3] >= t_coords[3])*t_coords[3]
    return [x1, y1, x2, y2]

def computeIOU(d_coords, t_coords):
    
    if len(d_coords) > 0 and len(t_coords) > 0:
        d_coords = cvtCoords(d_coords)
        t_coords = cvtCoords(t_coords)
        
        inter_coords = interCoords(d_coords, t_coords)
        inter_area = comArea(inter_coords)    
        union_area = comArea(d_coords) + comArea(t_coords) - inter_area
        #print(d_coords, t_coords, inter_area, comArea(d_coords), comArea(t_coords))
        IoU = inter_area/union_area
    else:
        IoU = 0
    return IoU   
            
def computeStats(gt_dict, pred_dict):
    fp_list = list()
    stats_dict = {'TP': 0, 'FP': 0, 'FN': 0}
    cluster_dict = dict()
    for frame in pred_dict:
        gt_frame = pred2GTindex(frame)
        #gt_frame = frame
        cluster_dict = updateClusterDict(gt_frame, gt_dict, cluster_dict)
        
        for p_obj in pred_dict[frame]:
            det = 0
            for cluster in cluster_dict:
                IoU = computeIOU(cluster_dict[cluster]['coords'], p_obj)
                if IoU >= 0.5:
                    cluster_dict[cluster]['det'] = 1
                    det = 1
            if det == 0:
                stats_dict['FP'] += 1
                fp_list.append(frame)

            
        cluster_dict, stats_dict = final_updateCD(cluster_dict, stats_dict)
        
    return stats_dict, fp_list

if __name__ == '__main__':
    
    gt_path = './updated_json/gt_fn_full.json'
    pred_path = './updated_json/yolo_pred_fn_full.json'
    
    gt_dict = readJSON(gt_path)
    pred_dict = readJSON(pred_path)
    
    stats_dict, fp_list = computeStats(gt_dict, pred_dict)

