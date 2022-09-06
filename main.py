import subprocess
from mattermostdriver import Driver
from commands.weather import forecast_hourly, weather, forecast
from utils.caiyun import caiyun
caiyun()
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


caiyun()

foo.posts.create_post(options={
    'channel_id': channel_id,
    'message': '====== start forecasting ======'})

forecast_hourly(foo, channel_id)
weather(foo, channel_id)
forecast(foo, channel_id)

foo.posts.create_post(options={
    'channel_id': channel_id,
    'message': '====== end forecasting ======'})
