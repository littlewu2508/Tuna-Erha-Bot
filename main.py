import subprocess
from mattermostdriver import Driver
my_token = subprocess.run(['cat' , '/data/wuyy/matterbridge_token'], stdout=subprocess.PIPE)

foo = Driver({
    """
    Required options

    Instead of the login/password, you can also use a personal access token.
    If you have a token, you don't need to pass login/pass.
    It is also possible to use 'auth' to pass a auth header in directly,
    for an example, see:
    https://vaelor.github.io/python-mattermost-driver/#authentication
    """
    'url': 'localhost',
    'token': my_token.stdout.decode("utf-8").strip(),

    """
    Optional options

    These options already have useful defaults or are just not needed in every case.
    In most cases, you won't need to modify these, especially the basepath.
    If you can only use a self signed/insecure certificate, you should set
    verify to your CA file or to False. Please double check this if you have any errors while
    using a self signed certificate!
    """
    'scheme': 'http',
    'port': 443,
    'basepath': '/mm/api/v4',
    'verify': False,  # Or /path/to/file.pem
    # 'mfa_token': 'YourMFAToken',
    """
    Setting this will pass the your auth header directly to
    the request libraries 'auth' parameter.
    You probably only want that, if token or login/password is not set or
    you want to set a custom auth header.
    """
    'auth': None,
    """
    If for some reasons you get regular timeouts after a while, try to decrease
    this value. The websocket will ping the server in this interval to keep the connection
    alive.
    If you have access to your server configuration, you can of course increase the timeout
    there.
    """
    'timeout': 3,

    """
    This value controls the request timeout.
    See https://python-requests.org/en/master/user/advanced/#timeouts
    for more information.
    The default value is None here, because it is the default in the
    request library, too.
    """
    'request_timeout': 3,

    """
    To keep the websocket connection alive even if it gets disconnected for some reason you
    can set the  keepalive option to True. The keepalive_delay defines how long to wait in seconds
    before attempting to reconnect the websocket.
    """
    'keepalive': False,
    'keepalive_delay': 5,

    """
    This option allows you to provide additional keyword arguments when calling websockets.connect()
    By default it is None, meaning we will not add any additional arguments. An example of an
    additional argument you can pass is one used to  disable the client side pings:
    'websocket_kw_args': {"ping_interval": None},
    """
    'websocket_kw_args': None,

    """
    Setting debug to True, will activate a very verbose logging.
    This also activates the logging for the requests package,
    so you can see every request you send.

    Be careful. This SHOULD NOT be active in production, because this logs a lot!
    Even the password for your account when doing driver.login()!
    """
    'debug': False
})

"""
Most of the requests need you to be logged in, so calling login()
should be the first thing you do after you created your Driver instance.
login() returns the raw response.
If using a personal access token, you still need to run login().
In this case, does not make a login request, but a `get_user('me')`
and sets everything up in the client.
"""
foo.login()

"""
If you want to make a websocket connection to the mattermost server
you can call the init_websocket method, passing an event_handler.
Every Websocket event send by mattermost will be send to that event_handler.
See the API documentation for which events are available.
"""
# foo.init_websocket(event_handler)

# Use `disconnect()` to disconnect the websocket
# foo.disconnect()

# To upload a file you will need to pass a `files` dictionary
channel_id = foo.channels.get_channel_by_name_and_team_name('totelegram', 'town-square')['id']
file_id = foo.files.upload_file(
    channel_id=channel_id,
    files={'files': ("forecast.png", open("pic/1661335908.png", 'rb'))}
)['file_infos'][0]['id']


# track the file id and pass it in `create_post` options, to attach the file
foo.posts.create_post(options={
    'channel_id': channel_id,
    'message': 'This is a test message'})


# track the file id and pass it in `create_post` options, to attach the file
foo.posts.create_post(options={
    'channel_id': channel_id,
    'message': 'This is the rain forecast at THU',
    'file_ids': [file_id]})

# # If needed, you can make custom requests by calling `make_request`
# foo.client.make_request('post', '/endpoint', options=None, params=None, data=None, files=None, basepath=None)
# 
# # If you want to call a webhook/execute it use the `call_webhook` method.
# # This method does not exist on the mattermost api AFAIK, I added it for ease of use.
# foo.webhooks.call_webhook('myHookId', options) # Options are optional
