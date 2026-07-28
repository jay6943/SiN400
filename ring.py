import dat
import cfg
import dev
import dxf
import tip


def rings(x, y, radius, length):
  r = cfg.radius
  cfg.radius = radius
  df = dev.euler(cfg.wg, cfg.radius, 180)

  dx = (length - cfg.ldcr) * 0.5
  x1, y1 = dev.bends(x + dx, y + cfg.sdcr, 180, 0, -1, 1)
  x2, y2 = dev.sline(x1, y1, cfg.ldcr)
  x3, y3 = dev.bends(x2, y2, 180, 0,  1, -1)
  x4, y4 = dev.sline(x3, y3, -cfg.ldcr)
  x5, y5 = dev.sline(x, y, length)
  x6, y6 = dev.sline(x, y2 + cfg.sdcr, length)

  cfg.radius = r
  print(f'{(df.length + cfg.ldcr) * 2:0.2f}', end=', ')

  return x6, y6


def double_rings(x, y):
  r1, r2 = 131, 133
  length = 400 + cfg.ldcr
  df = dev.euler(cfg.wg, cfg.radius, 90)
  dy = 50
  angle = 12
  x0 = x + length
  x2, y21 = dev.sbend(x, y, angle, cfg.stap - dy * 0.5)
  x2, y22 = dev.sbend(x, y - dy, angle, dy * 0.5 - cfg.stap)
  x3, y31 = dev.sline(x2, y21, cfg.ltap)
  x3, y32 = dev.sline(x2, y22, cfg.ltap)
  x4, y41 = dev.sbend(x3, y31, angle, dy * 0.5 - cfg.stap)
  x4, y42 = dev.sbend(x3, y32, angle, cfg.stap - dy * 0.5)
  x1, y1 = rings(x4, y, r1, length)
  x2, y2 = rings(x4 - length, y1, r2, length)
  x3, y3 = dev.sline(x2, y2, 500)
  x4, y4 = dev.bends(x3, y3, 90, 0, 1, -1)
  x5, y5 = dev.tline(x4, y4, df.dy * 2 - y2 + y - dy)
  x6, y6 = dev.bends(x5, y5, 90, 270, -1, 1)
  x7, y7 = dev.sline(x6, y - dy, x4 - x6)
  return x1, y2

def device(x, y):
  x1, y1 = double_rings(x, y)
  return x1, y1


def chip(x, y):
  idev = len(dat.points)
  x1, y1 = device(x, y)
  x2, x3 = dxf.center(idev, x, x1, cfg.size)

  title = f'SPACING-{cfg.sdcr:.1f}'
  # tip.sline(x2, y, x)
  # tip.sline(x3, y, x + cfg.size)
  # tip.texts(x2, y1, x, title)
  # tip.texts(x3, y1, x + cfg.size, title)
  print(title)

  return x + cfg.size, y


def chips(x, y, ranges):
  var = cfg.sdcr
  for cfg.sdcr in ranges:
    _, y = chip(x, y + cfg.ch * 3)
  cfg.sdcr = var

  return x + cfg.size, y


if __name__ == '__main__':
  # chips(0, 0, dxf.arange(1.8, 2, 0.1))
  chip(0, 0)
  dev.saveas('ring')
