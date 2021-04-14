# -*- coding: utf-8 -*-
import vk_api
import config


vk_session = vk_api.VkApi(login=config.login, password=config.password)
vk = vk_session.get_api()

try:
    vk_session.auth(token_only=True)
    print("ok")
except vk_api.AuthError as error_connect:
    print(error_connect)

result = vk.photos.getWallUploadServer(gid=config.owner_id)
upload_url = result['upload_url']
img = {'photo':()}
print(upload_url)

def vk_post(id_group):
    vk_session.method('wall.post', {
        'owner_id': -id_group,
        'message': config.text_message,

    })


vk_post(config.owner_id)
