import traceback

from yangsuite import get_logger, get_path
from ysyangtree import TaskHandler, TaskException

from yang.connector import GnmiNotification

from ysdevices import YSDeviceProfile
from ysgnmi import gnmi_util
from ysgnmi.device_plugin import GnmiSession

log = get_logger(__name__)

try:
    from ystestmgr.rpcverify import RpcVerify
except ImportError:
    log.warning('Install yangsuite-testmanager for opfield verification')

    class RpcVerify:
        def process_operational_state(data, returns={}):
            return data


def get_capabilities(user, devprofile):
    """Get the gNMI capabilities from the given device profile.

    Args:
      devprofile (ysdevices.devprofile.YSDeviceProfile): Device to
        communicate with

    Raises:
      grpc.RpcError: in case of connection error

    Returns:
      dict: Representation of :class:`CapabilityResponse` protobuf.
    """
    try:
        session = GnmiSession.get(devprofile, user)
        caps = session.capabilities()
        stop_session(user, devprofile)
        if not caps:
            session.log.error('No capabilities returned.')
            raise Exception('No capabilities returned.')
        return caps
    except Exception as exc:
        stop_session(user, devprofile)
        raise exc


def get_request(user, devprofile, request):
    """Send a gNMI GET request to the given device.

    Args:
      devprofile (ysdevices.devprofile.YSDeviceProfile): Device to
        communicate with
      request (dict): Passed through as kwargs of :class:`GetRequest`
        constructor.

    Raises:
      grpc.RpcError: in case of a connection error
      ValueError: if request contains invalid values

    Returns:
      dict: Representation of :class:`GetResponse` protobuf
    """
    gnmi_string = ''
    if 'raw' not in request:
        try:
            if not request.get('modules'):
                return {'error': 'No data requested from model.'}

            origin = request.get('origin')
            prefix = request.get('prefix')

            gnmi_msgs = gnmi_util.get_messages(
                request.get('action', ''),
                request,
                prefix
            )
            if not gnmi_msgs:
                raise Exception('No Xpath defined for GET.')
            for msg in gnmi_msgs:
                xpaths = msg.get('get', [])
                if not xpaths:
                    log.error('No Xpath defined for GET.')
                    continue
                gnmi_xpath = gnmi_util.get_xpath_config(
                    xpaths,
                    origin
                )
                payload = gnmi_util.get_gnmi_request(
                    gnmi_xpath,
                    **request
                )
                gnmi_string += str(payload)
                gnmi_string += '\n'
                if request.get('run'):
                    session = GnmiSession.get(devprofile, user)
                    session.log.info('gNMI GET\n' + '=' * 8 + '\n{0}'.format(
                        gnmi_string
                    ))
                    response = session.gnmi.service.Get(payload)
                    session.log.info(
                        'gNMI GET Response\n' + '=' * 17 + '\n{0}'.format(
                            str(response)
                        )
                    )
                    decode_result = session.decode_notification(response, {})
                    session.log.info(
                        'gNMI Response value decoded\n' + '=' * 27 + '\n'
                    )
                    for result in decode_result:
                        if 'decode' in result:
                            session.results.append(result['decode'])
                        else:
                            session.results.append(result)
            if not request.get('run'):
                if not gnmi_string:
                    raise Exception(
                        'Build GET failed.  Check YANG Suite logs for details.'
                    )
                return gnmi_string
        except Exception as exc:
            log.error('GET request error: {0}\n'.format(str(exc)))
    else:
        raise Exception("Raw messages from UI not supported yet.")


def get_results(user, devprofile):
    session = GnmiSession.get(devprofile, user)
    notifier = session.active_notifications.get(session)
    if notifier:
        if notifier.result:
            session.results.append(str(notifier.result))
            notifier.result = []
        else:
            session.results.append('Waiting for notification')
        if notifier.time_delta and notifier.time_delta < notifier.stream_max:
            notifier.stop()
    return session.result_queue()


def set_request(user, devprofile, request):
    """Send a gNMI SET request to the given device.

    Args:
      devprofile (ysdevices.devprofile.YSDeviceProfile): Device to
        communicate with
      request (dict): Passed through as kwargs of :class:`SetRequest`
        constructor.

    Raises:
      grpc.RpcError: in case of a connection error

    Returns:
      dict: Representation of :class:`SetResponse` protobuf
    """
    if 'raw' not in request:
        try:
            gnmi_string = ''
            if not request.get('modules'):
                return {'error': 'No data requested from model.'}

            origin = request.get('origin')
            prefix = request.get('prefix')

            gnmi_msgs = gnmi_util.get_messages(
                request.get('action', ''),
                request,
                prefix
            )
            if not gnmi_msgs:
                raise Exception('No Xpath defined for SET.')
            for msg in gnmi_msgs:
                update = msg.get('update', [])
                replace = msg.get('replace', [])
                delete = msg.get('delete', [])
                if update:
                    update = gnmi_util.get_set_payload(
                        update, origin, request.get('encoding')
                    )
                if replace:
                    replace = gnmi_util.get_set_payload(
                        replace, origin, request.get('encoding')
                    )
                if delete:
                    delete = gnmi_util.get_xpath_config(
                        delete, origin
                    )
                payload = gnmi_util.set_gnmi_request(
                    update,
                    replace,
                    delete,
                    **request
                )
                gnmi_string += str(payload)
                gnmi_string += '\n'
                if request.get('run'):
                    session = GnmiSession.get(devprofile, user)
                    session.log.info('gNMI SET\n' + '=' * 8 + '\n{0}'.format(
                        str(payload)
                        )
                    )
                    response = session.gnmi.service.Set(payload)
                    session.log.info(
                        'gNMI SET Response\n' + '=' * 17 + '\n{0}'.format(
                            str(response)
                        )
                    )
                    decode_result = session.decode_notification(response, {})
                    session.log.info(
                        'gNMI SET Response decoded\n' + '=' * 25 + '\n'
                    )
                    session.results.append(decode_result)
            if not request.get('run'):
                if not gnmi_string:
                    raise Exception(
                        'Build SET failed.  Check YANG Suite logs for details.'
                    )
                return gnmi_string
        except Exception as exc:
            log.error('SET request error: {0}\n'.format(str(exc)))
    else:
        raise Exception("Raw messages from UI not supported yet.")


def subscribe_request(user, devprofile, request):
    if 'raw' not in request:
        gnmi_string = ''
        try:
            if not request.get('modules'):
                return {'error': 'No data requested from model.'}

            origin = request.get('origin')
            prefix = request.get('prefix')

            gnmi_msgs = gnmi_util.get_messages(
                request.get('action', ''),
                request,
                prefix
            )
            if not gnmi_msgs:
                raise Exception('No Xpath defined for SUBSCRIBE.')
            for msg in gnmi_msgs:
                xpaths = msg.get('subscribe', [])
                if not xpaths:
                    log.error('No Xpath defined for SUBSCRIBE.')
                    continue
                gnmi_xpath = gnmi_util.get_xpath_config(xpaths, origin)
                sample_interval = request.get('sample_interval')
                if sample_interval:
                    sample_interval = int(1e9) * int(sample_interval)
                    request['sample_interval'] = sample_interval
                else:
                    request['sample_interval'] = int(1e9) * 10
                payload = gnmi_util.subscribe_gnmi_request(
                    gnmi_xpath[0],
                    **request
                )
                gnmi_string += str(payload)
                gnmi_string += '\n'
                if request.get('run'):
                    session = GnmiSession.get(devprofile, user)
                    response = session.gnmi.service.Subscribe(
                        gnmi_util.iter_subscribe_request(payload)
                    )
                    msg = 'gNMI SUBSCRIBE Response\n' + '=' * 22 + '\n'
                    msg += str(response)
                    session.log.info(msg)
                    format = {
                        'subscribe_mode': request.get('subscribe_mode'),
                        'sub_mode': request.get('subscribe_sub_mode'),
                        'encoding': request.get('encoding').upper(),
                        'sample_interval': sample_interval,
                        'max_stream': int(request.get('max_stream', 0))
                    }

                    def verify(data, returns={}):
                        return 'Add opfield verifier'
                    # TODO: make better verify
                    request['returns'] = {}
                    request['verifier'] = verify
                    request['decode'] = verify
                    request['format'] = format
                    # "device" is first argument for thread so pop it out.
                    request.pop('device')
                    subscribe_thread = GnmiNotification(
                        session,
                        response,
                        **request
                    )
                    subscribe_thread.log = session.log
                    subscribe_thread.start()
                    subscribe_thread.event_triggered = True
                    session.active_notifications[session] = subscribe_thread
            if not request.get('run'):
                if not gnmi_string:
                    raise Exception(
                        'Build SUBSCRIBE failed.  Check YANG Suite logs '
                        'for details.'
                    )
                return gnmi_string
        except Exception as exc:
            log.error('SUBSCRIBE request error: {0}\n'.format(str(exc)))
    else:
        raise Exception("Raw messages from UI not supported yet.")


def stop_session(user, devprofile):
    """Stop subscribe threads, close channel, and remove session instance."""
    if isinstance(devprofile, YSDeviceProfile):
        device = devprofile.base.profile_name
    else:
        device = str(devprofile)
    log.info("Stopping session {0}:{1}".format(user, device))
    GnmiSession.close(user, devprofile)


def show_gnmi_replay(user, devprofile, request):
    """Return replay metadata formatted for gNMI protocol.

    Args:
      request (dict): Replay name and category.

    Raises:
      tasks.TaskException: in case of replay retreival error

    Returns:
      dict: Representation of :class:`GetResponse`, :class:`SetResponse`
    """
    # TODO: need variables from device or may fail on xpath
    request_dict = {}
    user = request.get('user')
    replay_name = request.get('replay')
    category = request.get('category')
    path = get_path('replays_dir', user=user)
    try:
        request['replay'] = TaskHandler.get_replay(path, category, replay_name)

        # TODO: construct from replay

    except Exception as exe:
        log.error("Failed to generate gNMI replay %s", replay_name)
        log.debug(traceback.format_exc())
        raise TaskException("Failed to generate gNMI replay {0}\n{1}".format(
                replay_name,
                str(exe)
            )
        )

    return request_dict


def run_gnmi_replay(user, devprofile, request):
    """Run a replay over gNMI protocol.

    Args:
      devprofile (ysdevices.devprofile.YSDeviceProfile): Device to
        communicate with
      request (dict): Replay name and category.

    Raises:
      grpc.RpcError: in case of a connection error

    Returns:
      dict: Representation of :class:`GetResponse`, :class:`SetResponse`
    """
    user = request.get('user', '')
    response = {}

    gen_request = show_gnmi_replay(request)
    if gen_request['action'] == 'set':
        response = set_request(devprofile, user, gen_request['request'])
    elif gen_request['action'] == 'get':
        response = set_request(devprofile, user, gen_request['request'])
    else:
        raise TypeError(
                'gNMI "{0}" not supported.'.format(gen_request['action'])
            )

    return str(response)
