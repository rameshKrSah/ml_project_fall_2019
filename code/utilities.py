
import numpy as np
import pandas as pd
from tensorflow import keras
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import clear_output
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels

def get_one_hot_target(target, n_classes):
    """
        @brief: Get One-Hot encoded arary at position target with size 1 * n_size

        @param: Target index and the size 

        @return: An array with all zeros except a 1 at index target

    """
    if target >= n_classes:
        print("Invalid index value for one-hot encoding")

    ret = np.zeros((1, n_classes), dtype=int)
    ret[0][target] = 1
    return ret

def get_target_score(target, predictions):
    '''
        @brief: Get the percentage of target in predictions
        
        @param: Target value and prediction list
        
        @return: Percentage
    '''
    total = len(predictions)
    count = 0
    for x in predictions:
        if x == target:
            count += 1
            
    return (count / total)


def show_adversarial_results(data):
    '''
        Print out the accuracy and loss value passed in a dictionary with epsilon
        values as keys.
    '''
    for k, v in zip(data.keys(), data.values()):
        print("Epsilon = {} \t Loss = {:.3f} \t Accuracy = {:.3f}".format(k, v[0], v[1] * 100))

def print_confusion_matrix(y_true, y_pred, class_names, title, activities, figsize = (12, 6), fontsize=10):
    """
    Arguments
    ---------
    y_true: list
        True class labels
    
    y_pred: list
        Predicted class labels
        
    class_names: list
        An ordered list of class names, in the order they index the given confusion matrix.

    title: string
        Title of the plot

    activities: list
        List of activities or class labels

    figsize: tuple
        A 2-long tuple
  
    """
    cf_mat = confusion_matrix(y_true, y_pred, class_names)
    df_cm = pd.DataFrame(cf_mat, index=class_names, columns=class_names)
    
    fig, ax = plt.subplots(figsize = figsize) 
    try:
        heatmap = sns.heatmap(df_cm, annot=True, fmt="d", cmap='Blues', ax=ax)
    except ValueError:
        raise ValueError("Confusion matrix values must be integers.")
    
    heatmap.yaxis.set_ticklabels(activities, rotation=0, ha='right', fontsize='large')
    heatmap.xaxis.set_ticklabels(activities, rotation=90, ha='right', fontsize='large')
    plt.title(title, fontsize='large')
    plt.show()
    
    return fig, ax

class PlotLosses(keras.callbacks.Callback):
    '''
    Plots the loss and accuracy of a model while training, dynamically.
    '''
    def __init__(self):
        self.i = 1
        self.epoch = []
        self.losses = []
        self.val_losses = []
        self.accu = []
        self.val_accu = []
        self.fig = plt.figure()
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)
        self.epoch.append(self.i)
        
        f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(15, 8))
        clear_output(wait=True)

        self.accu.append(logs.get('acc'))
        ax1.plot(self.epoch, self.accu, label="Acc")
        
        try:
            self.val_accu.append(logs.get('val_acc'))
            ax1.plot(self.epoch, self.val_accu, label="Val Acc")
        except:
            print("No Validation Accuracy Values")
            
        ax1.legend()
       
        self.losses.append(logs.get('loss'))
        ax2.plot(self.epoch, self.losses, label="Loss")

        try:
            self.val_losses.append(logs.get('val_loss'))
            ax2.plot(self.epoch, self.val_losses, label="Val Loss")
        except:
            print("No Validation Loss Values")
            
        ax2.legend()
        
        self.i += 1
        ax2.set_xlabel("Epoch")
        plt.show();