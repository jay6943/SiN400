import cfg
import dxf
import dev
import cdr
import tip


def cals():
  for r in cfg.rings:
    df = dev.euler(cfg.wg, r, 180)
    print(f'Ring length, {r}, {df.length * 2:0.2f}')


def rings(x, y, radius, sign):
  dx = 200
  r = cfg.radius
  cfg.radius = radius
  x1, y1 = dev.bends(x + dx, y + sign * cfg.sdcr, 180, 0, -1, sign)
  x2, y2 = dev.bends(x1, y1, 180, 0,  1, -sign)
  x3, y3 = dev.sline(x, y, dx * 2)
  x4, y4 = dev.sline(x, y1 + sign * cfg.sdcr, dx * 2)
  cfg.radius = r
  return x4, y4


def single_ring(x, y, radius):
  dy = 500
  df = dev.euler(cfg.wg, cfg.radius, 90)
  x1, y1 = rings(x, y, radius, 1)
  x2, y2 = dev.bends(x, y1, 90, 0, -1, 1)
  x3, y3 = dev.tline(x2, y2, dy - y1 + y - df.dy * 2)
  x4, y4 = dev.bends(x3, y3, 90, 270, 1, -1)
  return x4, y4


def single_rings(x, y, isdcr):
  m = 10
  sdcr = cfg.sdcr
  var = dxf.arange(isdcr, isdcr + 0.19, 0.02)
  for i, cfg.sdcr in enumerate(var[::-1]):
    x1, y1 = x + 700 * i + 1200, y + cfg.ch * (m - i)
    x2, y2 = single_ring(x1, y1, 132)
    title = f'{cfg.sdcr}'
    tip.texts(x1, y1, x, title)
    tip.texts(x2, y2, x + cfg.lchip, title)
  cfg.sdcr = sdcr
  return x, y + (m + 4) * cfg.ch


def double_rings(x, y):
  dy = 300
  df = dev.euler(cfg.wg, cfg.radius, 90)

  x1, y1 = cdr.coupler(x, y, 100, 50, 12)
  x11, y11 = rings(x1, y1, cfg.rings[0], 1)
  x12, y12 = rings(x1 - (x11 - x1), y11, cfg.rings[1], 1)
  x13, y13 = dev.sline(x12, y12, x11 - x12)
  x14, y14 = dev.bends(x13, y13, 90, 0, 1, -1)
  x15, y15 = dev.tline(x14, y14, df.dy * 2 - y12 + y)
  x16, y16 = dev.bends(x15, y15, 90, 270, -1, 1)
  x17, y17 = dev.sline(x16, y, x1 - x16)

  x21, y21 = dev.bends(x, y1, 90, 0, -1, 1)
  x22, y22 = dev.tline(x21, y21, y + dy - df.dy * 2)
  x23, y23 = dev.bends(x22, y22, 90, 270, 1, -1)
  x24, y24 = dev.sline(x23, y23, x13 - x23 + df.dx * 2 + 100)

  sdcr = cfg.sdcr
  cfg.sdcr = 1.8
  x31, y31 = rings(x24, y24, cfg.rings[2], -1)
  x32, y32 = dev.bends(x24, y31, 90, 0, -1, -1)
  x33, y33 = dev.tline(x32, y32, df.dy * 2 - y31 + y)
  x34, y34 = dev.bends(x33, y33, 90, 270, 1, 1)
  x35, y35 = dev.sline(x34, y34, x31 - x24)
  cfg.sdcr = sdcr

  return x35, y24


def chip(x, y):
  tip.chip(x, y, cfg.lchip)
  x11, y11 = x + 2500, y + cfg.ch * 0.5
  x12, y12 = cdr.coupler(x11, y11, 100, 50, 12)
  x21, y21 = x11, y11 + cfg.ch
  x22, y22 = double_rings(x21, y21)
  x31, y31 = x11 - 800, y21 + cfg.ch * 0.5
  x32, y32 = single_ring(x31, y31, cfg.rings[1])
  x41, y41 = x31 - 800, y31 + cfg.ch * 0.5
  x42, y42 = single_ring(x41, y41, cfg.rings[0])

  tip.sline(x11, y11, x)
  tip.sline(x12, y11, x + cfg.lchip)
  tip.sline(x11, y12, x)
  tip.sline(x12, y12, x + cfg.lchip)
  title = f'SPACING-{cfg.sdcr:.1f}'
  tip.sline(x21, y21, x)
  tip.sline(x22, y21, x + cfg.lchip)
  tip.texts(x22, y22, x + cfg.lchip, title)
  print(title)
  tip.sline(x31, y31, x)
  tip.sline(x32, y32, x + cfg.lchip)
  tip.sline(x41, y41, x)
  tip.sline(x42, y42, x + cfg.lchip)

  return x + cfg.lchip, y


def chips(x, y, ranges):
  for var in ranges:
    _, y = tip.refer(x, y + cfg.ch * 2)
    _, y = single_rings(x, y, var)

  return x + cfg.lchip, y


if __name__ == '__main__':
  cals()
  # chips(0, 0, dxf.arange(1.8, 2, 0.1))
  # chip(0, 0)
  single_rings(0, 0, 2.0)
  dev.saveas('ring')
