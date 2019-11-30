# import sys
# sys.path.append('.')
from utils import img_tools
make_post_thumb = img_tools.make_post_thumb


img_name = 'static/info/public_domain.jpg'


make_post_thumb(img_name, sizes=[[100, 100]])
