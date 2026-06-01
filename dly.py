import cfg
import ref
import dxf
import dev
import dci
import tip
import pad
import y2x2


class delayline:
  def __init__(self):
    # self.dx = 5610
    self.dx = 4610
    self.dy = 50
    self.dr = 50

    # self.rmax = 1350
    # self.xinit = 7800
    self.rmax = 2400
    self.xinit = 6800
    self.length = 0

  def inner(self, x, y):
    cfg.radius -= self.dr * 2
    df = dev.euler(cfg.wg, cfg.radius, 90)
    x1, y1 = dev.bends(x, y, 90, 0, 1, 1)
    x2, y2 = dev.tline(x1, y1, self.dy + self.dr * 3)
    x3, y3 = dev.bends(x2, y2, 90, 90, 1, 1)
    x4, y4 = dev.sline(x3, y3, -self.dx)
    x5, y5 = dev.bends(x4, y4, 90, 180, 1, 1)
    x6, y6 = dev.tline(x5, y5, 0 - self.dy - self.dr)
    x7, y7 = dev.bends(x6, y6, 90, 270, 1, 1)
    x8, y8 = dev.sline(x7, y7, self.dx)
    self.length += 2 * (self.dx + self.dy + 2 * self.dr + 2 * df.l)
    return x8, y8

  def center(self, x, y):
    cfg.radius -= self.dr * 2
    print('Center radius =', cfg.radius)
    df = dev.euler(cfg.wg, cfg.radius, 90)
    dl = df.dx - self.dx * 0.5
    x1, y1 = dev.bends(x, y, 90, 0, 1, 1)
    x2, y2 = dev.tline(x1, y1, self.dy + self.dr * 3)
    x3, y3 = dev.bends(x2, y2, 90, 90, 1, 1)
    x4, y4 = dev.sline(x3, y3, dl)
    x5, y5 = dev.bends(x4, y4, 90, 0, -1, -1)
    x6, y6 = dev.tline(x5, y5, 0 - self.dy - self.dr * 2)
    x7, y7 = dev.bends(x6, y6, 90, 90, 1, -1)
    x8, y8 = dev.sline(x7, y7, dl)
    self.length += 2 * (dl + self.dy + 2 * df.l) + 5 * self.dr
    return x8, y8

  def outer(self, x, y):
    cfg.radius += self.dr * 2
    df = dev.euler(cfg.wg, cfg.radius, 90)
    x1, y1 = dev.bends(x, y, 90, 0, -1, 1)
    x2, y2 = dev.tline(x1, y1, self.dy + self.dr)
    x3, y3 = dev.bends(x2, y2, 90, 90, -1, 1)
    x4, y4 = dev.sline(x3, y3, self.dx)
    x5, y5 = dev.bends(x4, y4, 90, 0, 1, -1)
    x6, y6 = dev.tline(x5, y5, 0 - self.dy - self.dr * 3)
    x7, y7 = dev.bends(x6, y6, 90, 90, 1, -1)
    x8, y8 = dev.sline(x7, y7, 0 - self.dx)
    self.length += 2 * (self.dx + self.dy + 2 * self.dr + 2 * df.l)
    return x8, y8

  def outest(self, x, y):
    cfg.radius += self.dr * 2
    df = dev.euler(cfg.wg, cfg.radius, 90)
    x1, y1 = dev.bends(x, y, 90, 0, -1, 1)
    x2, y2 = dev.tline(x1, y1, self.dy + self.dr)
    x3, y3 = dev.bends(x2, y2, 90, 90, -1, 1)
    x4, y4 = dev.sline(x3, y3, self.dx)
    x5, y5 = dev.bends(x4, y4, 90, 0, 1, -1)
    self.length += self.dx + self.dy + self.dr + 3 * df.l
    return x5, y5

  def outport(self, x, y, dy):
    cfg.radius = 150
    df = dev.euler(cfg.wg, cfg.radius, 90)
    x1, y1 = dev.tline(x, y, dy - y + df.dy)
    x2, y2 = dev.bends(x1, y1, 90, 270, 1, 1)
    self.length += dy - y + df.dy + df.l
    return x2, y2

  def device(self, x, y):
    m = int((self.rmax - 200) * 0.5 / self.dr)
    cfg.radius = self.rmax
    x1, y1 = x, y
    for i in range(m): x1, y1 = self.inner(x1, y1)
    x2, y2 = self.center(x1, y1)
    cfg.radius -= self.dr
    for i in range(m): x2, y2 = self.outer(x2, y2)
    x3, y3 = self.outest(x2, y2)
    x4, y4 = self.outport(x3, y3, y)
    return x4, y4


def dline(x, y):
  sf = delayline()
  x1, _ = sf.device(x + sf.xinit, y)
  length = sf.length + sf.xinit + x + cfg.size - x1

  cm = length * 1e-4
  ns = length * 1.601 / 3 * 1e-5
  title = f'{cm:.1f} cm, {ns:.1f} nsec'
  tip.texts(x + sf.xinit, y, x, title)
  tip.texts(x1, y, x + cfg.size, title)
  print('Delay length, time =', title)
  return x, y + cfg.sch * 10


def dlmzi(x, y):
  sf = delayline()
  x2, y2 = sf.device(x + sf.xinit, y)

  angle = 30
  df = dev.euler(cfg.wg, cfg.radius, angle)
  cf = dev.circular(cfg.wg, 5, 90)
  x3, y31, y32 = y2x2.device(x2, y - cfg.s2x2)
  x6, y3 = dci.device(x + sf.xinit, y, angle)
  dxf.bends('core', cf, x3, y32, 270, 1, -1)
  idev = len(ref.points)
  x4, y4 = dev.sbend(x2, y3, 30, cfg.sch - cfg.s2x2 * 2)
  x5, y5 = dxf.move(idev, x2, y3, x4, y4, x2 - x4, 0, 0)
  x7, y7 = dev.sline(x6, y3, x5 - x6 + x2 - x4)
  x8 = x6 + (x7 - x6 - cfg.lpad) * 0.5
  # pad.bends(x8, y3, -1)
  pad.electrode('metal', x8, y3, cfg.lpad, 6, -1)
  pad.electrode('edge', x8, y3, cfg.lpad, cfg.eg, -1)

  tip.texts(x + sf.xinit, y, x, '2 nsec')
  tip.texts(x3, y, x + cfg.size, '2 nsec')

  length = sf.length - (df.l * 4 + x3 - x2) + x4 - x3
  print(f'Line {length / 10000:.3f} ({3 * 2 * 10 / 1.601:.3f}) cm')

  return x, y + cfg.sch * 10


def chips(x, y):
  radius = cfg.radius
  dlmzi(x, y)
  dline(x, y + cfg.sch * 31)
  cfg.radius = radius
  return x, y


if __name__ == '__main__':
  filename = 'delay_line'
  chips(0, cfg.sch * 2)
  dev.filled(0, 0, 1)
  dev.saveas(filename)
  dev.dlayers(filename, 'rect', 'edge')
