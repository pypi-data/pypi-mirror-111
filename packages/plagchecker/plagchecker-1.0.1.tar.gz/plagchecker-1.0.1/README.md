The python package is focused on checking Plagiarism from covered content it is the extension of service offered by prepostseo (https://www.prepostseo.com/plagiarism-checker)

## Install

For installation one can proceed to https://pypi.org/project/plagchecker/ or can use 
```python
pip install plagchecker
```

## Usage

The package focus on usage for checking plagiarised content and amount of plagiarised content present in the data spread over upto 5000 words or less with non-premium version of https://www.prepostseo.com/plagiarism-checker

## Modules

### There is 1 module named __init__.py

#### Class currently present in module: Checker

##### initialization of class: Checker()

The constructor takes in 1 manadatry argument i.e the APIKEY provided by www.prepostseo.com by signning up for free version.

##### Methods: Total of 7 Methods are present in Class: Checker

###### Method 1: __init__(self,apiKey):

Method is default constructor of the class Checker and takes in 1 manadatry argument i.e the APIKEY from www.prepostseo.com 

###### Method 2: getDataLen(self,data):

Method returns boolean value based on the count of words present in data if count is less than or equal to 5000 words return True else False.

###### Method 3: response(self,data):

Method returns 2 (two) values in string format:
1. status code of the querry: i.e 200 for successful execution in string format.
2. json response received upon successful execution or empty string

###### Method 4: getPlagPercent(self):

The function is used to get the percentage of plagiarised content. It returns the %(percentage) value in string format

###### Method 5: getUniquePrecent(self):

The function is used to get the precentage of unique content present in the data. It returns the %(percentage) value in string format

###### Method 6: getSources(self):

The function is used to get the sources from where the content was taken if found plagiarised in the data. It returns sources in the form of a list.

###### Method 7: getDetails(self):

The function is used to get the additional details of individual querries in data. It returns the additional details in the form of list.

## Created & Maintained By

### [Shrey Patel](https://github.com/shrey82)

## Sponsor Me for my education

### [Sponsor Shrey via buymecoffee](https://www.buymeacoffee.com/shrey82)
### [Sponsor Shrey directly](https://rzp.io/l/shrey82)
<a href="https://www.linkedin.com/in/shrey-patel-7b7003161/" target="_blank"><img src="https://github.com/aritraroy/social-icons/blob/master/linkedin-icon.png?raw=true" width="60"></a><a href="https://instagram.com/s.h.r.e.y.82" target="_blank"><img src="https://github.com/aritraroy/social-icons/blob/master/instagram-icon.png?raw=true" width="60"></a><a href="https://github.com/shrey82" target="_blank"><img src="https://img.icons8.com/material-outlined/52/000000/github.png"></a>

