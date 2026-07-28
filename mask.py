import cfg
import dxf
import dev
import key
import pbs
import tip
import tap
import fgc
import y4x4
import rx


def polarization_beam_splitter(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 0)
  _, y = tip.refer(x, y + cfg.ch * 2)
  _, y = pbs.polarizer(x, y + cfg.ch, 1)
  _, y = pbs.chips(x, y, dxf.arange(12, 100, 2))
  _, y = pbs.polarizer(x, y + cfg.ch, -1)
  _, y = tip.refer(x, y)


def hybrid(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 0)
  _, y = tip.refer(x, y + cfg.ch * 2)
  _, y = pbs.polarizer(x, y + cfg.ch, 1)
  _, y = y4x4.chips(x, y, dxf.arange(150, 167, 1))
  _, y = pbs.polarizer(x, y, -1)
  _, y = tip.refer(x, y)


def waveguide(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 0)
  _, y = tip.refer(x, y + cfg.ch * 2)
  _, y = pbs.polarizer(x, y + cfg.ch, 1)
  _, y = tip.chips(x, y, dxf.arange(0.2, 0.4, 0.01))
  _, y = tap.chips(x, y, dxf.arange(1.2, 2.6, 0.1))
  _, y = fgc.chips(x, y)
  _, y = pbs.polarizer(x, y, -1)
  _, y = tip.refer(x, y)


def icr(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 0)
  rx.chips(x, y + cfg.size * 0.5)
  dev.split('metal', 0, -1)


def grating(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y, 0)
  fgc.chips(x, y + cfg.ch * 2)


def chips(region):
  if 0 in region: key.cross(0, 0)
  if 1 in region: waveguide(-1, 1)
  if 2 in region: polarization_beam_splitter(1, 1)
  if 3 in region: hybrid(-1, -1)
  if 4 in region: icr(-1, 1)


if __name__ == '__main__':
  cfg.draft = 'draft'
  filename = f'SiN400_V{cfg.ver}_{cfg.draft}'
  chips([0, 1, 2, 3])
  # dev.savedxf(filename)
  dev.saveas(filename)
  dev.dlayers(filename, 'rect', 'edge')
  dev.dlayers(filename, 'hole', 'bars')
  if cfg.draft in ['draft']: dev.gdstext(filename)
