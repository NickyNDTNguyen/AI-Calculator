# week_8
## AI Calculator
![](https://i.imgur.com/esKBcPn.png)

- In this project, we will take a photo and determine all digit and simple operators in this photo.
- Our model will predict the digits and operators, then return a result of this calculation.

## Our team
#### Nguyen Hong Hai - nguyen.honghai.hv@gmail.com
#### Nguyen Dang Thanh Nguyen - ndtnguyen130@gmail.com
#### Nguyen Hanh Tu - tu.hanh.nguyen@outlook.com



## Dataset
![](https://i.imgur.com/hwAtC38.png)
- https://drive.google.com/open?id=1i8lIDKPC9Rxt-UEc3VqA30ydEeSbNSHN
- We used a dataset from Kaggle.com but before applying it in our model, we had to reduce amount of data (just take only + - * /)



## Model
![](https://i.imgur.com/kMfw73z.png)
- We have decided to use MobileNet_V2.
- But during training process, we speacially have concentrated on ImageGenerator steps. For data digit we just use **Rescale, rotation_range**
- We should not use any flips here because it does not make sense for digit, moreover, it can make your result goes wrong. Ex: 2 and 5
