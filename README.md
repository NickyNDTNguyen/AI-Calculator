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
- We used a dataset from Kaggle.com but before appling it in our model, we had to reduce amount of data (just take only + - * /)



## Model
![](https://i.imgur.com/kMfw73z.png)
- We have decided to use MobileNet_V2.
- But during training process, we speacially have concentrated on ImageGenerator steps. For data digit we just use **Rescale, rotation_range**
- We should not use any flips here because it does not make sense for digit, moreover, it can make your result goes wrong. Ex: 2 and 5
- Final accuracy: 60%

![](https://i.imgur.com/r6ayxOV.png)
### {'+': 0, '-': 1, '0': 2, '1': 3, '2': 4, '3': 5, '4': 6, '5': 7, '6': 8, '7': 9, '8': 10, '9': 11, 'div': 12, 'times': 13}
```python
def convert_math(math_detect):
    for i in range(0, len(math_detect)):
        if math_detect[i] == 0:
            math_detect[i] = '+'
        elif math_detect[i] == 1:
            math_detect[i] = '-'
        elif math_detect[i] == 2:
            math_detect[i] = '0'
        elif math_detect[i] == 3:
            math_detect[i] = '1'
        elif math_detect[i] == 4:
            math_detect[i] = '2'
        elif math_detect[i] == 5:
            math_detect[i] = '3'
        elif math_detect[i] == 6:
            math_detect[i] = '4'
        elif math_detect[i] == 7:
            math_detect[i] = '5'
        elif math_detect[i] == 8:
            math_detect[i] = '6'
        elif math_detect[i] == 9:
            math_detect[i] = '7'
        elif math_detect[i] == 10:
            math_detect[i] = '8'
        elif math_detect[i] == 11:
            math_detect[i] = '9'
        elif math_detect[i] == 12:
            math_detect[i] = '/'
        elif math_detect[i] == 13:
            math_detect[i] = '*'
    return math_detect
```
## Calculate
```python
def calculate_string(math_detect):
    math_detect = convert_math(math_detect)
    calculator = ''.join(str(item) for item in math_detect)
    print(calculator + ' = ' + str(eval(calculator)))
```
```
3*6 = 18
```

## DEMO
...
