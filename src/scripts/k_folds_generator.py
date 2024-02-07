import datetime
import shutil
from pathlib import Path
from collections import Counter

import yaml
import numpy as np
import pandas as pd
from ultralytics import YOLO
from sklearn.model_selection import KFold

#https://docs.ultralytics.com/es/guides/kfold-cross-validation/

#Cargar el dataset y las labels
dataset_path = Path('./data/data_pcb/segmented_k_folds') 
labels = sorted(dataset_path.rglob("*labels/*.txt"))

#Cargar el yaml con los nombres de las clases
yaml_file = './data/data_pcb/segmented_k_folds/data.yaml'
with open(yaml_file, 'r', encoding="utf8") as y:
    classes = yaml.safe_load(y)['names']
cls_idx = list(range(len(classes))) 

#Inicializamos una tabla de pandas segun las medidas de uestros datos
indx = [l.stem for l in labels]
labels_df = pd.DataFrame([], columns=cls_idx, index=indx)

#Por cada label hacemo one hot encoding
for label in labels:
    lbl_counter = Counter()
    with open(label,'r') as lf:
        lines = lf.readlines()
    # classes for YOLO label uses integer at first position of each line
    for l in lines:
        lbl_counter[int(l.split(' ')[0])] += 1
    labels_df.loc[label.stem] = lbl_counter
#Correjimos los valores nulos
labels_df = labels_df.fillna(0.0)

print(labels_df)

#Dividimos segun k_folds
ksplit = 3 #Nuemro de divisiones del k-folds
kf = KFold(n_splits=ksplit, shuffle=True, random_state=20) #Indicamos que las divisiones son aletorias shuffle=True
kfolds = list(kf.split(labels_df))

#Convertimos los resultado en dataframes por separado
folds = [f'split_{n}' for n in range(1, ksplit + 1)]
folds_df = pd.DataFrame(index=indx, columns=folds)
for idx, (train, val) in enumerate(kfolds, start=1):

    folds_df.loc[labels_df.iloc[train].index, f'split_{idx}'] = 'train'
    folds_df.loc[labels_df.iloc[val].index, f'split_{idx}'] = 'val'

print(folds_df)

#Se calcula el ratio de distribucion para cada etiqueta en cada distribucion (lo ideal es que fueran lo mas parecidas posibles, se necesitan mas datos)
fold_lbl_distrb = pd.DataFrame(index=folds, columns=cls_idx)
for n, (train_indices, val_indices) in enumerate(kfolds, start=1):
    train_totals = labels_df.iloc[train_indices].sum()
    val_totals = labels_df.iloc[val_indices].sum()
    # To avoid division by zero, we add a small value (1E-7) to the denominator
    ratio = val_totals / (train_totals + 1E-7)
    fold_lbl_distrb.loc[f'split_{n}'] = ratio

print(fold_lbl_distrb)

#Generamos los directorios y los yamls segun las divisiones
supported_extensions = ['.jpg', '.jpeg', '.png']
# Initialize an empty list to store image file paths
images = []
# Loop through supported extensions and gather image files
for ext in supported_extensions:
    images.extend(sorted((dataset_path / 'images').rglob(f"*{ext}")))
# Create the necessary directories and dataset YAML files (unchanged)
save_path = Path(dataset_path / 'Fold_Cross_val')
save_path.mkdir(parents=True, exist_ok=True)
ds_yamls = []
for split in folds_df.columns:
    # Create directories
    split_dir = save_path / split
    split_dir.mkdir(parents=True, exist_ok=True)
    (split_dir / 'train' / 'images').mkdir(parents=True, exist_ok=True)
    (split_dir / 'train' / 'labels').mkdir(parents=True, exist_ok=True)
    (split_dir / 'val' / 'images').mkdir(parents=True, exist_ok=True)
    (split_dir / 'val' / 'labels').mkdir(parents=True, exist_ok=True)
    # Create dataset YAML files
    dataset_yaml = split_dir / f'{split}_dataset.yaml'
    ds_yamls.append(dataset_yaml)
    with open(dataset_yaml, 'w') as ds_y:
        yaml.safe_dump({
            'path': split_dir.as_posix(),
            'train': 'train',
            'val': 'val',
            'names': classes
        }, ds_y)

print(folds_df.columns)

#Por utlimo copiamos los datos a los nuevos directorioss
for image, label in zip(images, labels):
    for split, k_split in folds_df.loc[image.stem].items():
        # Destination directory
        img_to_path = save_path / split / k_split / 'images'
        lbl_to_path = save_path / split / k_split / 'labels'

        # Copy image and label files to new directory (SamefileError if file already exists)
        shutil.copy(image, img_to_path / image.name)
        shutil.copy(label, lbl_to_path / label.name)

