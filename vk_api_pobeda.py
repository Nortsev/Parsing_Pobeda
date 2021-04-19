# -*- coding: utf-8 -*-
import vk_api
from typing import List
import config


def create_session(login, password):
    vk_session = vk_api.VkApi(login=login, password=password)
    try:
        vk_session.auth(token_only=True)
        print("ok")
    except vk_api.AuthError as error_connect:
        print(error_connect)
    return vk_session


def upload_photo(vk_session, photo_path: str, caption: str, album_id: str):
    upload = vk_api.VkUpload(vk_session)
    vk_photo = upload.photo(photos=[photo_path], album_id=album_id,
                            caption=[caption])[0]
    return f'photo{vk_photo["owner_id"]}_{vk_photo["id"]}'


def post_wall(vk_session, owner_id: int, text_message: str, vk_photos: List[str]):
    vk_photos_id = ",".join(vk_photos)
    vk_post = vk_session.method('wall.post', {
        'owner_id': -owner_id,
        'message': text_message,
        'attachments': vk_photos_id  # 'photo615022059_457240069,photo615022059_457240054'
    })
    return vk_post


def post_group_wall(photos_path: list, captions: list, album_id: str):
    vk_session = create_session(login=config.login, password=config.password)
    vk_photos_id = [upload_photo(vk_session, photo_path, caption, album_id) for photo_path, caption in zip(photos_path,
                                                                                                           captions)]
    vk_post = post_wall(vk_session, config.owner_id, config.text_message, vk_photos_id)
    return vk_post


