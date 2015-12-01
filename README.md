python-ocr
==========

#### How to use

1. To train it, add your .ttf font file in the /fonts directory and run `python train.py font-name`
2. (optional) Run `python generate-sentence.py font-name font-size` if you wish to generate a test image to be read
3. Run `python ocr.py image.png` to run

Currently works with upper case characters and one line of text.

#### Requirements

- Python 2.7 or 3.4+
- Imagemagick
- Python PIL

#### Sample

This image:

![screenshot](https://raw.github.com/lucasdnd/python-ocr/master/image.png)

Will generate this output:

```
T - 94.7222222222% sure
H - 96.9444444444% sure
E - 96.8181818182% sure
 
Q - 84.3813387424% sure
U - 92.876344086% sure
I - 98.3333333333% sure
C - 87.1527777778% sure
K - 76.0256410256% sure
 
B - 90.4347826087% sure
R - 90.1282051282% sure
O - 87.9310344828% sure
W - 80.0854700855% sure
N - 87.9166666667% sure
 
F - 99.2063492063% sure
O - 87.9310344828% sure
X - 86.049382716% sure
 
J - 87.6660341556% sure
U - 89.9193548387% sure
M - 87.816091954% sure
P - 94.5454545455% sure
S - 83.984375% sure
 
O - 85.9913793103% sure
V - 87.037037037% sure
E - 88.9393939394% sure
R - 84.6153846154% sure
 
T - 90.4166666667% sure
H - 90.8333333333% sure
E - 96.5151515152% sure
 
L - 97.0175438596% sure
A - 88.024691358% sure
Z - 88.75% sure
Y - 88.2142857143% sure
 
D - 90.8% sure
O - 86.8534482759% sure
G - 86.3839285714% sure
```
