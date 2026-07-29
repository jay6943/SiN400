import cfg
import dxf
import dev
import tip


def coupler(x, y, length, height, angle):
  dy = (height - cfg.sdcr) * 0.5
  x2, y2a = dev.sbend(x, y, angle, dy)
  x2, y2b = dev.sbend(x, y + height, angle, -dy)
  if length > 0:
    x3, y3a = dev.sline(x2, y2a, length)
    x3, y3b = dev.sline(x2, y2b, length)
  else:
    x3, y3a, y3b = x2, y2a, y2b
  x4, y4a = dev.sbend(x3, y3a, angle, -dy)
  x4, y4b = dev.sbend(x3, y3b, angle, dy)
  return x4, y4b


def chips(x, y, ranges):
  sdcr = cfg.sdcr
  for i, cfg.sdcr in enumerate(ranges):
    x1, y1 = x + 4500, y + (i + 1) * cfg.ch
    x2, y2 = coupler(x1, y1, 100, 50, 12)
    tip.sline(x1, y1, x)
    tip.sline(x2, y1, x + cfg.lchip)
    tip.sline(x1, y2, x)
    tip.sline(x2, y2, x + cfg.lchip)
    dev.texts(x + 4750, y1 - 25, f'{cfg.sdcr:.2f}', 0.3, 'cc')
  cfg.sdcr = sdcr
  return x2, y2


if __name__ == '__main__':
  chips(0, 0, dxf.arange(1.7, 2.2, 0.1))
  dev.saveas('coupler')
