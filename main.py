import subprocess
from mattermostdriver import Driver
my_token = subprocess.run(['cat' , '/data/wuyy/matterbridge_token'], stdout=subprocess.PIPE)

foo = Driver({
    'url': 'localhost',
    'token': my_token.stdout.decode("utf-8").strip(),
    'scheme': 'http',
    'port': 8065,
    'basepath': '/mm/api/v4',
    'verify': False,  # Or /path/to/file.pem
    'auth': None,
    'timeout': 3,
    'request_timeout': 3,
    'keepalive': False,
    'keepalive_delay': 5,
    'websocket_kw_args': None,
    'debug': False
})

foo.login()

channel_id = foo.channels.get_channel_by_name_and_team_name('totelegram', 'town-square')['id']
file_id = foo.files.upload_file(
    channel_id=channel_id,
    files={'files': ("forecast.png", open("pic/1661335908.png", 'rb'))}
)['file_infos'][0]['id']


foo.posts.create_post(options={
    'channel_id': channel_id,
    'message': 'This is a test message'})

foo.posts.create_post(options={
    'channel_id': channel_id,
    'message': 'This is the rain forecast at THU',
    'file_ids': [file_id]})
