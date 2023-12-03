# Handwritten detector 

In this notebook, we'll go through the steps of training a CRNN (CNN + RNN) model for handwriting recognition. The model will be trained using the CTC (Connectionist Temporal Classification) loss.

## TODO list for documentation: 
- [ ] Plotting unreadable data -- show proofing that some data in the data set may be unreadable and that we are taking care of it in our code
- [ ] Explaining why we needed to preprocess and prepare the images for training. Explain the shapes of the images
- [ ] Explain the whole CTC loss thing 
- [ ] Explain the model architecture. Why were the layers that were used used ? Why we did that, why we did this ? 
- [x] Show-proof the whole characters' situation of decoding and encoding. Add some test scenarios.
- [ ] Add test scenarios for each of the features.
- [ ] Explain the whole training variables that were used. What's the meaning and the goal of each one ?

## Q&A 
- Why did I use jupyter notebook instead of anything else ? 
- Why did I use python for the whole project ? 
- 

## CHARACTER ENCODING AND DECODING 

| Character | Encoding |
|-----------|----------|
| A         | 0        |
| B         | 1        |
| C         | 3        |
| D         | 4        |
| E         | 5        |
| F         | 6        |
| G         | 7        |
| H         | 8        |
| I         | 9        |
| J         | 10       |
| K         | 11       |
| L         | 12       |
| M         | 13       |
| N         | 14       |
| O         | 15       |
| P         | 16       |
| Q         | 17       |
| R         | 18       |
| S         | 19       |
| T         | 20       |
| U         | 21       |
| V         | 22       |
| W         | 23       |
| X         | 24       |
| Y         | 25       |
| Z         | 26       |
| -         | 26       |
|           | 28       |


Enncoding and decoding functions (and how they work)

```python3
# -------- testing the conversion from labels to nums --------
test_name = "TOMICI-VLAD"
print(test_name)
print(label2Num(test_name))
```

## Data preparation 

#### 1) Removing unnecessary data from the dataset
```python3
# -------- plotting unreadable data --------
for i in range(6):
    ax = plt.subplot(2, 3, i+1)
    img_path = f"data/train_v2/train/{unreadable.loc[i, 'FILENAME']}"
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    plt.imshow(image, cmap='gray')
    plt.title(unreadable.loc[i, 'IDENTITY'], fontsize=12)
    plt.axis('off')

plt.subplots_adjust(wspace=0.2, hspace=0.8)
```


#### 2) Preprocessing images before training
- the images are loaded as grayscale and reshaped to (256, 64)
- the width and height are cropped if they are greater than 256 and 64 respectively; if they're smaller the image is padded with white pixels; finally the image is rotated clockwise to bring the image shape to (x, y)
- the image is then normalized to range [0, 1]



## About the training variables
- **train_y**: contains the true labels converted to numbers and padded with -1; the length of each label is max_str_length
- **train_label_len**: contains the length of each true label (without padding)
- **train_input_len**: contains the length of each predicted label; the length of all the predicted labels is constant
- **train_output**: is a dummy output for the ctc loss


```python3
# -------- testing the train_y --------
print(f"True label : {train.loc[100, 'IDENTITY']}")
print(f"train_y : {train_y[100]}")
print(f"train_label_len : {train_label_len[100]}")
print(f"train_input_len : {train_input_len[100]}")
```

## The model architecture 

![The model architecture](images/model-architecture.png)

```shell
Model: "model_5"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 input (InputLayer)          [(None, 256, 64, 1)]      0         
                                                                 
 conv1 (Conv2D)              (None, 256, 64, 32)       320       
                                                                 
 batch_normalization_9 (Batc  (None, 256, 64, 32)      128       
 hNormalization)                                                 
                                                                 
 activation_9 (Activation)   (None, 256, 64, 32)       0         
                                                                 
 max1 (MaxPooling2D)         (None, 128, 32, 32)       0         
                                                                 
 conv2 (Conv2D)              (None, 128, 32, 64)       18496     
                                                                 
 batch_normalization_10 (Bat  (None, 128, 32, 64)      256       
 chNormalization)                                                
                                                                 
 activation_10 (Activation)  (None, 128, 32, 64)       0         
                                                                 
 max2 (MaxPooling2D)         (None, 64, 16, 64)        0         
                                                                 
 dropout_6 (Dropout)         (None, 64, 16, 64)        0         
                                                                 
 conv3 (Conv2D)              (None, 64, 16, 128)       73856     
                                                                 
 batch_normalization_11 (Bat  (None, 64, 16, 128)      512       
 chNormalization)                                                
                                                                 
 activation_11 (Activation)  (None, 64, 16, 128)       0         
                                                                 
 max3 (MaxPooling2D)         (None, 64, 8, 128)        0         
                                                                 
 dropout_7 (Dropout)         (None, 64, 8, 128)        0         
                                                                 
 reshape (Reshape)           (None, 64, 1024)          0         
                                                                 
 dense1 (Dense)              (None, 64, 64)            65600     
                                                                 
 lstm1 (Bidirectional)       (None, 64, 512)           657408    
                                                                 
 lstm2 (Bidirectional)       (None, 64, 512)           1574912   
                                                                 
 dense2 (Dense)              (None, 64, 30)            15390     
                                                                 
 softmax (Activation)        (None, 64, 30)            0         
                                                                 
=================================================================
Total params: 2,406,878
Trainable params: 2,406,430
Non-trainable params: 448
_________________________________________________________________
```

(The output shape of the predictions is (64, 30). The model predicts words of 64 characters and each
character contains the probability of the 30 alphabets which we defined earlier.)
