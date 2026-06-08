import cfg
import dxf
import gds
import dev
import fgc


def bends(path):
  wg, angle = cfg.wg - cfg.dw, 6
  df = dev.curve(wg, cfg.radius, angle)
  x1, y1 = dxf.srect('core', 0, 0, 10, wg)
  x2, y2 = dxf.bends('core', df, x1, y1, 0, 1, 1)
  dxf.tilts('core', x2, y2, 10, wg, angle)
  gds.savelayer(f'{path}/{cfg.radius:.0f}r_{angle:.0f}deg')


def sbend(path):
  wg = cfg.wg - cfg.dw
  angle = 25
  dy = 50
  dl = 10
  length = 250

  df = dev.curve(wg, cfg.radius, angle)
  x1, y1 = dxf.srect('core', -dl, 0, dl, wg)
  x2, y2 = dxf.sbend('core', df, x1, y1, dy)
  dxf.srect('core', x2, y2, length - x2, wg)
  gds.savelayer(f'{path}/{cfg.radius:.0f}r_{dy:.0f}h')


def ubend(path):
  wg, length = cfg.wg - cfg.dw, 20
  df = dev.curve(wg, cfg.radius, 180)
  x1, y1 = dxf.srect('core', 0, 0, length, wg)
  x1, y1 = dxf.bends('core', df, x1, y1, 0, 1, 1)
  dxf.srect('core', x1, y1, -length, wg)
  gds.savelayer(f'{path}/{cfg.radius:.0f}r_180a')


def dc(path):
  wg = cfg.wg - cfg.dw
  df = dev.curve(wg, cfg.radius, 30)
  dxf.bends('core', df, 0, 0, 0, -1, -1)
  dxf.bends('core', df, 0, 0, 0, 1, -1)
  gds.savelayer(f'{path}/dc{cfg.radius:.0f}r')


def grating_coupler(path):
  fgc.grating('core', 0, 0, 1, 0)
  dxf.srect('core', -10, 0, 10, cfg.wg - cfg.dw)
  gds.savelayer(f'{path}/grating_{cfg.period}_{cfg.duty}')


if __name__ == '__main__':
  cfg.draft = 'mask'
  workspace = '../../ansys'
  # bends(f'{workspace}/euler')
  # ubend(f'{workspace}/euler')
  # sbend(f'{workspace}/euler')
  grating_coupler(f'{workspace}/Grating coupler/SiN-2.6')
