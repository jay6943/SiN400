import cfg
import dxf
import dev
import key
import pbs
import tip
import tap
import grc
import sdc
import y4x4
import ring
import rx


def polarization_beam_splitter(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = tip.refer(x, y + cfg.ch * 2)
  _, y = pbs.polarizer(x, y + cfg.ch, 1)
  _, y = pbs.chips(x, y, 12, 100, 2)
  _, y = pbs.polarizer(x, y + cfg.ch, -1)
  _, y = tip.refer(x, y)


def optical_hybrid(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = tip.refer(x, y + cfg.ch * 2)
  _, y = pbs.polarizer(x, y + cfg.ch, 1)
  _, y = y4x4.chips(x, y, 152, 164, 1)
  _, y = pbs.polarizer(x, y, -1)
  _, y = tip.refer(x, y)
  _, y = sdc.chips(x, y, 1.5, 2.1, 0.05)


def waveguide(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = tip.refer(x, y + cfg.ch * 2)
  _, y = pbs.polarizer(x, y + cfg.ch, 1)
  _, y = tip.chips(x, y, 0.2, 0.4, 0.01)
  _, y = tap.chips(x, y, 1.2, 2.6, 0.1)
  _, y = grc.chips(x, y, 0.48, 0.52, 0.01)
  _, y = pbs.polarizer(x, y, -1)
  _, y = tip.refer(x, y)


def rings(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  _, y = ring.chips(x, y, 1.3, 1.55, 0.05)


def icr(xpos, ypos):
  x, y = key.frame(xpos, ypos, 1)
  x, y = dev.filled(x, y)
  rx.chips(x, y + cfg.lchip * 0.5)
  dev.split('metal', 0, -1)


def chips(region):
  if 0 in region: key.cross(0, 0)
  if 1 in region: waveguide(-1, 1)
  if 2 in region: polarization_beam_splitter(1, 1)
  if 3 in region: optical_hybrid(-1, -1)
  if 4 in region: rings(1, -1)


if __name__ == '__main__':
  cfg.draft = 'draft'
  filename = f'SiN400_V{cfg.ver}_{cfg.draft}'
  chips([0, 1, 2, 3, 4])
  dev.saveas(filename)
  dev.dlayers(filename, 'rect', 'edge')
  dev.dlayers(filename, 'hole', 'bars')
  if cfg.draft in ['draft']: dev.gdstext(filename)
