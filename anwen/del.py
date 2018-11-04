# class SharesHandler(CommonResourceHandler):
#     res = Share

#     def pre_post(self, json_arg):
#         new_obj = self.res()
#         new_obj.update(json_arg)
#         if self.res.by_slug(new_obj.slug):
#             self.send_error(409)
#         else:
#             new_obj.save()
#             return new_obj
