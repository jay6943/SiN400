import os

ver = '1.0'
path = f'../../mask/SiN400-{ver}'
if not os.path.isdir(path): os.mkdir(path)
draft = 'draft'

wg = 1.0
eg = 40.0
ch = 100.0
radius = 150.0
angle = 6.0

w1x2 = 5.6
l1x2 = 18.0
s1x2 = 1.5
w2x2 = 8.4
l2x2 = 52.0
s2x2 = 1.46
w4x4 = 12.0
l4x4 = 159.0
s4x4 = 1.5
lpbs = 65.0
wpbs = 1.85
ltpr = 5.0
wtpr = 2.0
ltip = 600.0
lext = 500.0
wtip = 0.3
lpad = 400.0
wpad = 10.0
stap = 1.9
ltap = 100
ldcr = 20
sdcr = 2.0

duty = 0.5
period = 1.4

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
