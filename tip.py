import cfg
import dxf
import dev


def device(x, y, sign):
  w = [cfg.wg, cfg.wtip]
  l = [cfg.ltip - cfg.lext, cfg.lext]

  x1, _ = dxf.taper('core', x, y, sign * l[0], w[0], w[1])
  x2, _ = dxf.srect('core', x1, y, sign * l[1], w[1])
  dxf.srect('edge', x, y, x2 - x, cfg.eg)
  
  return x2, y


def sline(x, y, xend):
  sign = 1 if xend > x else -1
  if sign * (xend - x) > cfg.ltip:
    x1, _ = dev.sline(x, y, xend - x - sign * cfg.ltip)
  else: x1 = x
  x2, _ = device(x1, y, sign)
  return x2, y


def texts(x, y, xend, title):
  if xend > x: sign, align = 1, 'lc'
  else: sign, align = -1, 'rc'
  x1, _ = sline(x, y, xend)
  dev.texts(x1 - sign * cfg.ltip, y - cfg.sch * 0.5, title, 0.3, align)
  return x1, y


def chip(x, y, lchip):
  x1 = x + cfg.ltip
  x2, _ = dev.sline(x1, y, lchip - 2 * cfg.ltip)
  device(x1, y, -1)
  device(x2, y,  1)
  return x + lchip, y


def chips(x, y):
  y += cfg.sch
  wtip = cfg.wtip
  for cfg.wtip in dxf.arange(0.2, 0.4, 0.02):
    chip(x, y, cfg.size)
    title = f'TIP-{cfg.wtip:.2f}'
    dev.texts(x + cfg.ltip, y - cfg.sch * 0.5, title, 0.3, 'rc')
    dev.texts(x + cfg.size - cfg.ltip, y - cfg.sch * 0.5, title, 0.3, 'lc')
    y += cfg.sch
  cfg.wtip = wtip
  return x + cfg.size, y


if __name__ == '__main__':
  chips(0, 0)
  dev.saveas('tip')
