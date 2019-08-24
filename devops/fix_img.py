

# import sys
# sys.path.append('.')
from utils import img_tools
make_post_thumb = img_tools.make_post_thumb


img_name = 'static/avatar/feed_152.png'


make_post_thumb(img_name, sizes=[[132, 132]])
