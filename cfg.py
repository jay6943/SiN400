import os

ver = '1.0'
path = f'../../mask/SiN400-{ver}'
if not os.path.isdir(path): os.mkdir(path)
draft = 'draft'

dw = 0.1
wg = 0.8 + dw
eg = 40
ch = 250
sch = 100
radius = 150
angle = 6

w1x2 = 5.6 + dw
l1x2 = 18.3
s1x2 = 1.5
w2x2 = 8.4 + dw
l2x2 = 52.5
s2x2 = 1.46
w4x4 = 12 + dw
l4x4 = 581
s4x4 = 1.5
lpbs = 56
wpbs = 1.85 + dw
ltpr = 5
wtpr = 2.0 + dw
ltip = 600
lext = 500
wtip = 0.3
lpad = 400
wpad = 10
ldci = 22.3
sdci = 1.9

duty = 0.5
period = 1.0

size = 10000
wkey = 400
wbar = 250
tkey = wkey + wbar
lkey = size + wkey
lbar = size + wkey + wbar
skey = size + wkey + wbar * 2
area = [[0, 0], [-1, 0], [0, 0], [-1, -1], [0, -1]]

labels = {
  'core': 1,
  'edge': 2,
  'keys': 3,
  'bars': 4,
  'cross': 5,
  'metal': 6,
  'hole': 7,
  'rect': 8,
  'text': 9
}
