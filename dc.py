import cfg
import dat
import dxf
import dev
import tip


def coupler(x, y):
  length = 100

  x1, y1 = dev.sline(x, y + cfg.sdcr * 0.5, length)
  x1, y2 = dev.sline(x, y - cfg.sdcr * 0.5, length)

  return x1, y1, y2


def chip(x, y, lchip):
  angle = 20
  ch = cfg.ch * 0.5
  dy = ch - cfg.sdcr * 0.5
  y1 = y + ch
  y2 = y - ch

  idev = len(dat.points)
  x1, _ = dev.sbend(x, y1, angle, -dy)
  x1, _ = dev.sbend(x, y2, angle, dy)
  x2, y3, y4 = coupler(x1, y)
  x3, _ = dev.sbend(x2, y3, angle, dy)
  x3, _ = dev.sbend(x2, y4, angle, -dy)
  x5, x6 = dxf.center(idev, x, x3, lchip)

  title = f'DC-{cfg.sdcr:.1f}'
  tip.texts(x5, y1, x, title)
  tip.sline(x5, y2, x)
  tip.texts(x6, y1, x + lchip, title)
  tip.sline(x6, y2, x + lchip)
  print(f'{title}, chip length ~ {x6 - x5:.0f} um')

  return x + lchip, y


def chips(x, y, ranges):
  sdcr = cfg.sdcr
  y += cfg.ch * 1.5
  for cfg.sdcr in ranges:
    _, y = chip(x, y, cfg.lchip)
    y += cfg.ch * 2
  cfg.sdcr = sdcr

  return x + cfg.lchip, y - cfg.ch * 0.5


if __name__ == '__main__':
  chips(0, 0, dxf.arange(1.7, 2.2, 0.1))
  dev.saveas('dc')
