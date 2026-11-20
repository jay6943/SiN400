import cfg
import dat
import dxf
import dev
import tip


def chip(x, y, lchip):
  angle, dy = 15, cfg.ch * 0.5 - cfg.s1x2

  idev = len(dat.points)
  x1, y1, y2 = dxf.device(x, y, 1)
  x2, y1 = dev.sbend(x1, y1, angle,  dy)
  x2, y2 = dev.sbend(x1, y2, angle, -dy)
  x5, x6 = dxf.center(idev, x, x2, lchip)

  title = f'1x2-{cfg.l1x2:.1f}'
  tip.sline(x5, y, x, title)
  tip.sline(x6, y1, x + lchip, title)
  tip.sline(x6, y2, x + lchip, '')
  print(f'{title}; {x6 - x5:.0f}')

  return x + lchip, y


def chips(x, y, ranges):
  y += cfg.ch * 1.5
  l1x2 = cfg.l1x2
  for cfg.l1x2 in ranges:
    _, y = chip(x, y, cfg.lchip)
    y += cfg.ch * 2
  cfg.l1x2 = l1x2

  return x + cfg.lchip, y


if __name__ == '__main__':
  chips(0, 0, dxf.arange(16, 20, 0.5))
  dev.saveas(f'1x2_{cfg.draft}')
