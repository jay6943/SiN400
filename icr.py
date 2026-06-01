import cfg
import dev
import pbs
import voa
import tip
import y4x4


def tap(x, y, dy):
  df = dev.euler(cfg.wg, cfg.radius, 90)
  x1, y1 = dev.bends(x, y, 90, 0, 1, -1)
  dev.bends(x, y, 90, 0, -1, -1)
  dev.tline(x1, y1, df.dy - dy)


def tbend(x, y, xsign, ysign, length):
  dq = ysign * (45 + 45 * (1 - xsign))
  x1, y1 = dev.bends(x, y, 45, 0, xsign, ysign)
  if length > 0: x1, y1 = dev.tilts(x1, y1, length, cfg.wg, dq)
  x2, y2 = dev.bends(x1, y1, 45, 45, xsign, ysign)
  return x2, y2


def att(x, y, df):
  x1, y1 = dev.bends(x, y, 90, 0, 1, 1)
  x2, y2 = dev.tline(x1, y1, 700)
  x3, y3 = dev.bends(x2, y2, 90, 90, -1, 1)
  x3, y3 = dev.sline(x3, y3, 100)
  x4, y4 = voa.device(x3, y3)
  x4, y4 = dev.sline(x4, y4, 100)
  x5, y5 = dev.bends(x4, y4, 90, 0, 1, -1)
  x5, y5 = dev.tline(x5, y5, -150)
  x6, y6 = dev.bends(x5, y5, 90, 90, 1, -1)
  x7, y7 = dev.sline(x6, y6, x3 - x4 + 100)
  x8, y8 = dev.bends(x7, y7, 90, 0, -1, -1)
  x8, y8 = dev.tline(x8, y8, y - y8 + df.dy)
  x9, y9 = dev.bends(x8, y8, 90, 270, 1, 1)
  return x9, y


def chip(x, y, xsize, ysize, ytap):
  dy = cfg.ch * 2
  ch = cfg.ch * 0.5
  df = dev.euler(cfg.wg, cfg.radius, 90)

  x1, y1 = att(x + cfg.ltip, y + ch, df)
  x1, y2 = dev.sline(x + cfg.ltip, y - ch, x1 - x - cfg.ltip)
  tap(x + 800, y2 - cfg.sdci, ysize - ytap)

  x3, y31, y32 = pbs.device('core', x1, y1)
  x3, y33, y34 = pbs.device('core', x1, y2)

  x41, y41 = dev.sbend(x3, y31, 90, y + dy + ch - y31)
  x42, y42 = tbend(x3, y32, 1, -1, ch - cfg.sch * 0.5)
  x43, y43 = tbend(x3, y33, 1,  1, ch - cfg.sch * 0.5)
  x44, y44 = dev.sbend(x3, y34, 90, y - dy - ch - y34)

  _, y52 = dev.tline(x42, y42, y - dy + ch - y42 + df.dy)
  _, y53 = dev.tline(x43, y43, y + dy - ch - y43 - df.dy)

  x5, _ = dev.bends(x43, y53, 90, 90, -1,  1)
  x5, _ = dev.bends(x42, y52, 90, 90, -1, -1)

  dev.sline(x41, y41, x5 - x41)
  dev.sline(x44, y44, x5 - x44)

  cfg.l4x4 = 578
  x11, y11 = y4x4.device(x5, y + dy, cfg.ch)
  cfg.l4x4 = 584
  x12, y12 = y4x4.device(x5, y - dy, cfg.ch)

  tip.sline(x + cfg.ltip, y1, x)
  tip.sline(x + cfg.ltip, y2, x)
  for i in [-3, -1, 1, 3]:
    x13, _ = tip.sline(x11, y11 + i * ch, x + xsize)
    x13, _ = tip.sline(x12, y12 + i * ch, x + xsize)

  print(f'RX; {int(x11 - x1)} {int(x13 - x)}')

  return x + xsize, y


def chips(x, y):
  xsize = cfg.size * 0.5
  ysize = 1600
  ytap = 475

  chip(x, y, xsize, ysize, ytap)

  dev.sline(x, y + ysize, xsize)
  dev.sline(x, y - ysize + ytap, xsize)


if __name__ == '__main__':
  chips(0, cfg.size * 0.5)
  dev.filled(0, 0, 1)
  dev.saveas('icr')
  dev.dlayers('icr', 'rect', 'edge')
  # dev.savedxf('icr')
