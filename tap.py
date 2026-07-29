import cfg
import dat
import dxf
import dev
import tip


def device(x, y, angle):
  dev.bends(x, y + cfg.sdcr, angle, 0, -1, 1)
  x1, y1 = dev.sbend(x, y + cfg.sdcr, angle, cfg.ch - cfg.sdcr)
  dev.sline(x, y, x1 - x)
  return x1, y1


def chip(x, y, lchip):
  idev = len(dat.points)
  x1, _ = device(x, y, 30)
  x2, x3 = dxf.center(idev, x, x1, lchip)

  title = f'TAP-{cfg.sdcr:.1f}'
  tip.texts(x2, y, x, title)
  tip.texts(x3, y, x + lchip, title)
  tip.sline(x3, y + cfg.ch, x + lchip)
  print(title)

  return x, y


def chips(x, y, ranges):
  sdcr = cfg.sdcr
  y -= cfg.ch * 2
  for cfg.sdcr in ranges:
    _, y = chip(x, y + cfg.ch * 2, cfg.lchip)
  cfg.sdcr = sdcr
  return x, y + cfg.ch


if __name__ == '__main__':
  chips(0, 0, dxf.arange(1.5, 2.5, 0.1))
  dev.saveas('tap')
