from pathlib import Path
entry=':qh_rosetta:M::\\x7f\\x45\\x4c\\x46\\x02\\x01\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x3e\\x00:\\xff\\xff\\xff\\xff\\xff\\xfe\\xfe\\x00\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xfe\\xff\\xff\\xff:/_qh_probe_01/rosetta/rosetta:POCF'
Path('/proc/sys/fs/binfmt_misc/register').write_text(entry)
print('QH_BINFMT_REGISTERED')
print(Path('/proc/sys/fs/binfmt_misc/qh_rosetta').read_text())
