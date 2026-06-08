import sys
import cfg
import ref
import dxf
import dev
import dci
import tip
import pad
import y2x2


class delayline:
  def __init__(self, x, dx, dy, dr, rmax):
    self.xp = x
    self.dx = dx
    self.dy = dy
    self.dr = dr
    self.rmax = rmax
    self.radius = cfg.radius
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
    print('Center radius =', cfg.radius, 'um')
    df = dev.euler(cfg.wg, cfg.radius, 90)
    dl = self.dx * 0.5 - df.dx
    if dl < 10:
      print(f'Error!, Ceneter line < {dl:.3f} um')
      sys.exit()
    else: print(f'Center line = {dl:.3f} um')
    x1, y1 = dev.bends(x, y, 90, 0, 1, 1)
    x2, y2 = dev.tline(x1, y1, self.dy + self.dr * 3)
    x3, y3 = dev.bends(x2, y2, 90, 90, 1, 1)
    x4, y4 = dev.sline(x3, y3, -dl)
    x5, y5 = dev.bends(x4, y4, 90, 0, -1, -1)
    x6, y6 = dev.tline(x5, y5, 0 - self.dy - self.dr * 2)
    x7, y7 = dev.bends(x6, y6, 90, 90, 1, -1)
    x8, y8 = dev.sline(x7, y7, -dl)
    self.length += 2 * (self.dy + 2 * df.l - dl) + 5 * self.dr
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
    return x5, y5, y4

  def outport(self, x, y, dy):
    df = dev.euler(cfg.wg, cfg.radius, 90)
    x1, y1 = dev.tline(x, y, dy - y + df.dy)
    x2, y2 = dev.bends(x1, y1, 90, 270, 1, 1)
    self.length += dy - y + df.dy + df.l
    return x2, y2

  def device(self, x, y):
    num = int((self.rmax - cfg.radius - 200) * 0.5 / self.dr) + 1
    print('Rounds =', num)
    cfg.radius = self.rmax
    x1, y1 = x, y
    for _ in range(num): x1, y1 = self.inner(x1, y1)
    x2, y2 = self.center(x1, y1)
    cfg.radius -= self.dr
    for _ in range(num): x2, y2 = self.outer(x2, y2)
    x3, y3, y4 = self.outest(x2, y2)
    cfg.radius = self.radius
    x4, _ = self.outport(x3, y3, y)
    return x4, y4


def chip(x, y):
  sf = delayline(8200, 6800, 100, 50, 1000)
  x1, y1 = sf.device(x + sf.xp, y)
  sf.length = (sf.length + sf.xp + x + cfg.size - x1) * 1e-4
  tip.texts(x + sf.xp, y, x, f'{sf.length:.3f}')
  tip.texts(x1, y, x + cfg.size, f'{sf.length:.3f}')
  print('Length =', f'{sf.length:.3f} cm')
  
  return x, y1


if __name__ == '__main__':
  filename = 'dly'
  chip(0, 0)
  # dev.savedxf(filename)
  dev.filled(0, 0)
  dev.saveas(filename)
  dev.dlayers(filename, 'rect', 'edge')
