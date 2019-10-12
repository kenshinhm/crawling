import os
from PIL import Image

cur_dir = os.getcwd()
src_dir = os.path.join(cur_dir, 'src')
dst_dir = os.path.join(cur_dir, 'dst')
start_idx = 755

for root, dirs, files in os.walk(src_dir):
    for idx, file in enumerate(files):
        im = Image.open(os.path.join(src_dir, file))
        target_name = '{}.png'.format(start_idx+idx)
        im.save(os.path.join(dst_dir, target_name))


