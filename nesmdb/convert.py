import cPickle as pickle
import os

import numpy as np
from scipy.io.wavfile import write as wavwrite
from scipy.misc import imsave as imwrite

import nesmdb.vgm
import nesmdb.score


def _verify_type(fp, expected):
  fn = os.path.basename(fp)
  num_ext = expected.count('.')
  failed = False

  try:
    fp_exts = fn.rsplit('.', num_ext)[-num_ext:]
    expected_exts = expected.rsplit('.', num_ext)[-num_ext:]
    assert fp_exts == expected_exts
  except:
    raise Exception('Expected {} filetype; specified {}'.format(expected, fp))


# VGM Simplifiers


def vgm_simplify(in_fp, out_fp, vgm_simplify_nop1, vgm_simplify_nop2, vgm_simplify_notr, vgm_simplify_nono):
  with open(in_fp, 'rb') as f:
    vgm = f.read()

  vgm, _ = nesmdb.vgm.vgm_simplify(vgm, vgm_simplify_nop1, vgm_simplify_nop2, vgm_simplify_notr, vgm_simplify_nono)

  with open(out_fp, 'wb') as f:
    f.write(vgm)


def vgm_shorten(in_fp, out_fp, vgm_shorten_start, vgm_shorten_nmax):
  with open(in_fp, 'rb') as f:
    vgm = f.read()

  vgm = nesmdb.vgm.vgm_shorten(vgm, vgm_shorten_nmax, vgm_shorten_start)

  with open(out_fp, 'wb') as f:
    f.write(vgm)


# NES disassembly raw


def vgm_to_ndr(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    vgm = f.read()

  ndr = nesmdb.vgm.vgm_to_ndr(vgm)

  with open(out_fp, 'wb') as f:
    pickle.dump(ndr, f)


def ndr_to_txt(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    ndr = pickle.load(f)

  txt = nesmdb.vgm.nd_to_txt(ndr)

  with open(out_fp, 'w') as f:
    f.write(txt)


def txt_to_ndr(in_fp, out_fp):
  with open(in_fp, 'r') as f:
    txt = f.read()

  ndr = nesmdb.vgm.txt_to_nd(txt)

  with open(out_fp, 'wb') as f:
    pickle.dump(ndr, f)


def ndr_to_vgm(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    ndr = pickle.load(f)

  vgm = nesmdb.vgm.ndr_to_vgm(ndr)

  with open(out_fp, 'wb') as f:
    f.write(vgm)


# NES disassembly functional


def vgm_to_ndf(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    vgm = f.read()

  ndr = nesmdb.vgm.vgm_to_ndr(vgm)
  ndf = nesmdb.vgm.ndr_to_ndf(ndr)

  with open(out_fp, 'wb') as f:
    pickle.dump(ndf, f)


def ndf_to_txt(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    ndf = pickle.load(f)

  txt = nesmdb.vgm.nd_to_txt(ndf)

  with open(out_fp, 'w') as f:
    f.write(txt)


def txt_to_ndf(in_fp, out_fp):
  with open(in_fp, 'r') as f:
    txt = f.read()

  ndf = nesmdb.vgm.txt_to_nd(txt)

  with open(out_fp, 'wb') as f:
    pickle.dump(ndf, f)


def ndf_to_vgm(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    ndf = pickle.load(f)

  ndr = nesmdb.vgm.ndf_to_ndr(ndf)
  vgm = nesmdb.vgm.ndr_to_vgm(ndr)

  with open(out_fp, 'wb') as f:
    f.write(vgm)


# NES-MDB score formats


def ndf_to_exprsco(in_fp, out_fp, ndf_to_exprsco_rate):
  with open(in_fp, 'rb') as f:
    ndf = pickle.load(f)

  rawsco = nesmdb.score.ndf_to_rawsco(ndf)
  exprsco = nesmdb.score.rawsco_to_exprsco(rawsco)
  exprsco = nesmdb.score.exprsco_downsample(exprsco, ndf_to_exprsco_rate, False)

  with open(out_fp, 'wb') as f:
    pickle.dump(exprsco, f)


def ndf_to_midi(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    ndf = pickle.load(f)

  rawsco = nesmdb.score.ndf_to_rawsco(ndf)
  exprsco = nesmdb.score.rawsco_to_exprsco(rawsco)
  midi = nesmdb.score.exprsco_to_midi(exprsco)

  with open(out_fp, 'wb') as f:
    f.write(midi)


def exprsco_to_seprsco(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    exprsco = pickle.load(f)

  seprsco = nesmdb.score.exprsco_to_seprsco(exprsco)

  with open(out_fp, 'wb') as f:
    pickle.dump(seprsco, f)


def exprsco_to_blndsco(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    exprsco = pickle.load(f)

  blndsco = nesmdb.score.exprsco_to_blndsco(exprsco)

  with open(out_fp, 'wb') as f:
    pickle.dump(blndsco, f)


# WAV converters


def _f32_to_i16(wav):
  wav *= 32767.
  wav = np.clip(wav, -32767., 32767.)
  wav = wav.astype(np.int16)

  return wav


def vgm_to_wav(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    vgm = f.read()

  wav = nesmdb.vgm.vgm_to_wav(vgm)

  wavwrite(out_fp, 44100, _f32_to_i16(wav))


def ndr_to_wav(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    ndr = pickle.load(f)

  vgm = nesmdb.vgm.ndr_to_vgm(ndr)
  wav = nesmdb.vgm.vgm_to_wav(vgm)

  wavwrite(out_fp, 44100, _f32_to_i16(wav))


def ndf_to_wav(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    ndf = pickle.load(f)

  ndr = nesmdb.vgm.ndf_to_ndr(ndf)
  vgm = nesmdb.vgm.ndr_to_vgm(ndr)
  wav = nesmdb.vgm.vgm_to_wav(vgm)

  wavwrite(out_fp, 44100, _f32_to_i16(wav))


def midi_to_wav(in_fp, out_fp, midi_to_wav_rate=None):
  with open(in_fp, 'rb') as f:
    midi = f.read()

  exprsco = nesmdb.score.midi_to_exprsco(midi)
  if midi_to_wav_rate is not None:
    exprsco = nesmdb.score.exprsco_downsample(exprsco, midi_to_wav_rate, False)
  rawsco = nesmdb.score.exprsco_to_rawsco(exprsco)
  ndf = nesmdb.score.rawsco_to_ndf(rawsco)
  ndr = nesmdb.vgm.ndf_to_ndr(ndf)
  vgm = nesmdb.vgm.ndr_to_vgm(ndr)
  wav = nesmdb.vgm.vgm_to_wav(vgm)

  wavwrite(out_fp, 44100, _f32_to_i16(wav))


def exprsco_to_wav(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    exprsco = pickle.load(f)

  rawsco = nesmdb.score.exprsco_to_rawsco(exprsco)
  ndf = nesmdb.score.rawsco_to_ndf(rawsco)
  ndr = nesmdb.vgm.ndf_to_ndr(ndf)
  vgm = nesmdb.vgm.ndr_to_vgm(ndr)
  wav = nesmdb.vgm.vgm_to_wav(vgm)

  wavwrite(out_fp, 44100, _f32_to_i16(wav))


def seprsco_to_wav(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    seprsco = pickle.load(f)

  exprsco = nesmdb.score.seprsco_to_exprsco(seprsco)
  rawsco = nesmdb.score.exprsco_to_rawsco(exprsco)
  ndf = nesmdb.score.rawsco_to_ndf(rawsco)
  ndr = nesmdb.vgm.ndf_to_ndr(ndf)
  vgm = nesmdb.vgm.ndr_to_vgm(ndr)
  wav = nesmdb.vgm.vgm_to_wav(vgm)

  wavwrite(out_fp, 44100, _f32_to_i16(wav))


def blndsco_to_wav(in_fp, out_fp):
  with open(in_fp, 'rb') as f:
    blndsco = pickle.load(f)

  exprsco = nesmdb.score.blndsco_to_exprsco(blndsco)
  rawsco = nesmdb.score.exprsco_to_rawsco(exprsco)
  ndf = nesmdb.score.rawsco_to_ndf(rawsco)
  ndr = nesmdb.vgm.ndf_to_ndr(ndf)
  vgm = nesmdb.vgm.ndr_to_vgm(ndr)
  wav = nesmdb.vgm.vgm_to_wav(vgm)

  wavwrite(out_fp, 44100, _f32_to_i16(wav))


if __name__ == '__main__':
  import argparse
  import os
  import sys
  import traceback

  from tqdm import tqdm

  parser = argparse.ArgumentParser()

  conversion_to_types = {
      # VGM simplifiers
      'vgm_simplify': ('.vgm', '.simp.vgm'),
      'vgm_shorten': ('.vgm', '.short.vgm'),

      # NES disassembly raw
      'vgm_to_ndr': ('.vgm', '.ndr.pkl'),
      'ndr_to_txt': ('.ndr.pkl', '.ndr.txt'),
      'txt_to_ndr': ('.ndr.txt', '.ndr.pkl'),
      'ndr_to_vgm': ('.ndr.pkl', '.ndr.vgm'),

      # NES disassembly functional
      'vgm_to_ndf': ('.vgm', '.ndf.pkl'),
      'ndf_to_txt': ('.ndf.pkl', '.ndf.txt'),
      'txt_to_ndf': ('.ndf.txt', '.ndf.pkl'),
      'ndf_to_vgm': ('.ndf.pkl', '.ndf.vgm'),

      # NES-MDB score formats
      'ndf_to_exprsco': ('.ndf.pkl', '.exprsco.pkl'),
      'ndf_to_midi': ('.ndf.pkl', '.mid'),
      'exprsco_to_seprsco': ('.exprsco.pkl', '.seprsco.pkl'),
      'exprsco_to_blndsco': ('.exprsco.pkl', '.blndsco.pkl'),

      # WAV converters
      'vgm_to_wav': ('.vgm', '.wav'),
      'ndr_to_wav': ('.ndr.pkl', '.wav'),
      'ndf_to_wav': ('.ndf.pkl', '.wav'),
      'midi_to_wav': ('.mid', '.wav'),
      'exprsco_to_wav': ('.exprsco.pkl', '.wav'),
      'seprsco_to_wav': ('.seprsco.pkl', '.wav'),
      'blndsco_to_wav': ('.blndsco.pkl', '.wav'),
  }

  conversion_to_kwargs = {
      'vgm_simplify': ['vgm_simplify_nop1', 'vgm_simplify_nop2', 'vgm_simplify_notr', 'vgm_simplify_nono'],
      'vgm_shorten': ['vgm_shorten_start', 'vgm_shorten_nmax'],
      'ndf_to_exprsco': ['ndf_to_exprsco_rate'],
      'midi_to_wav': ['midi_to_wav_rate'],
  }

  parser.add_argument('conversion', type=str, choices=conversion_to_types.keys())
  parser.add_argument('fps', type=str, nargs='+')
  parser.add_argument('--out_dir', type=str)
  parser.add_argument('--skip_verify', action='store_true', dest='skip_verify')
  parser.add_argument('--vgm_shorten_start', type=int)
  parser.add_argument('--vgm_shorten_nmax', type=int)
  parser.add_argument('--vgm_simplify_nop1', action='store_true', dest='vgm_simplify_nop1')
  parser.add_argument('--vgm_simplify_nop2', action='store_true', dest='vgm_simplify_nop2')
  parser.add_argument('--vgm_simplify_notr', action='store_true', dest='vgm_simplify_notr')
  parser.add_argument('--vgm_simplify_nono', action='store_true', dest='vgm_simplify_nono')
  parser.add_argument('--ndf_to_exprsco_rate', type=float)
  parser.add_argument('--midi_to_wav_rate', type=float)

  parser.set_defaults(
      conversion=None,
      fps=None,
      out_dir=None,
      skip_verify=False,
      vgm_shorten_start=None,
      vgm_shorten_nmax=1024,
      vgm_simplify_nop1=False,
      vgm_simplify_nop2=False,
      vgm_simplify_notr=False,
      vgm_simplify_nono=False,
      ndf_to_exprsco_rate=None,
      midi_to_wav_rate=None)

  args = parser.parse_args()

  in_type, out_type = conversion_to_types[args.conversion]
  fps = args.fps

  if len(fps) > 1 and args.out_dir is None:
    raise Exception('Must specify output directory for batch mode')

  if len(fps) == 1 and args.out_dir is None:
    out_fps = [fps[0].replace(in_type, out_type)]
  else:
    out_fns = [os.path.basename(fp).replace(in_type, out_type) for fp in fps]
    out_fps = [os.path.join(args.out_dir, fn) for fn in out_fns]

    if os.path.exists(args.out_dir):
      print 'WARNING: Output directory {} already exists'.format(args.out_dir)
    else:
      os.makedirs(args.out_dir)

  for in_fp, out_fp in tqdm(zip(fps, out_fps)):
    if not args.skip_verify:
      _verify_type(in_fp, in_type)
      _verify_type(out_fp, out_type)

    kwargs = {}
    if args.conversion in conversion_to_kwargs:
      kwargs = {kw:getattr(args, kw) for kw in conversion_to_kwargs[args.conversion]}

    try:
      globals()[args.conversion](in_fp, out_fp, **kwargs)
    except:
      print '-' * 80
      print in_fp
      traceback.print_exc()
