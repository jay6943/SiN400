import cfg
import dxf
import gds
import dev
import fgc


def bends(path):
  angle = 6
  df = dev.curve(cfg.wg, cfg.radius, angle)
  x1, y1 = dxf.srect('core', 0, 0, 10, cfg.wg)
  x2, y2 = dxf.bends('core', df, x1, y1, 0, 1, 1)
  dxf.tilts('core', x2, y2, 10, cfg.wg, angle)
  gds.savelayer(f'{path}/{cfg.radius:.0f}r_{angle:.0f}deg')


def sbend(path):
  angle, dy, dl, length = 25, 50, 10, 250
  df = dev.curve(cfg.wg, cfg.radius, angle)
  x1, y1 = dxf.srect('core', -dl, 0, dl, cfg.wg)
  x2, y2 = dxf.sbend('core', df, x1, y1, dy)
  dxf.srect('core', x2, y2, length - x2, cfg.wg)
  gds.savelayer(f'{path}/{cfg.radius:.0f}r_{dy:.0f}h')


def ubend(path):
  length = 20
  df = dev.curve(cfg.wg, cfg.radius, 180)
  x1, y1 = dxf.srect('core', 0, 0, length, cfg.wg)
  x1, y1 = dxf.bends('core', df, x1, y1, 0, 1, 1)
  dxf.srect('core', x1, y1, -length, cfg.wg)
  gds.savelayer(f'{path}/{cfg.radius:.0f}r_180a')


def dc(path):
  df = dev.curve(cfg.wg, cfg.radius, 30)
  dxf.bends('core', df, 0, 0, 0, -1, -1)
  dxf.bends('core', df, 0, 0, 0, 1, -1)
  gds.savelayer(f'{path}/dc{cfg.radius:.0f}r')


def grating_coupler(path):
  fgc.grating('core', 0, 0, 1, 0)
  dxf.srect('core', -10, 0, 10, cfg.wg)
  gds.savelayer(f'{path}/grating_{cfg.period}')


if __name__ == '__main__':
  cfg.draft = 'mask'
  workspace = '../../ansys'
  # bends(f'{workspace}/euler')
  # ubend(f'{workspace}/euler')
  # sbend(f'{workspace}/euler')
  grating_coupler(f'{workspace}/Grating coupler/SiN-2.6')
