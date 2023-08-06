import json
import asyncio
import logging
import traceback
import janus
from requests.structures import CaseInsensitiveDict
from localstack.utils.common import TMP_THREADS, short_uid, wait_for_port_open
from localstack.utils.async_utils import receive_from_queue, get_named_event_loop, run_sync

LOG = logging.getLogger(__name__)

# maps connection ID to websocket channel details
WEBSOCKET_CHANNELS = {}


def start_websocket_server(port, message_handler, connection_events=False):
    # keep this import here for python 2 compatibility!
    import websockets
    loop = get_event_loop()

    async def return_response(result, connection_id):
        if result is not None:
            q_outgoing = WEBSOCKET_CHANNELS[connection_id]['outgoing']
            await q_outgoing.async_q.put(result)

    async def handle_incoming(websocket, connection_id, path):
        channel_details = WEBSOCKET_CHANNELS[connection_id]
        try:
            async for msg in websocket:
                try:
                    msg = json.loads(msg)
                except Exception as e:
                    LOG.debug('Unable to parse incoming websockets message as JSON: %s' % e)
                try:
                    # invoke handler function to get message response
                    result = await run_sync(message_handler, message=msg, connection_id=connection_id,
                        path=path, headers=CaseInsensitiveDict(websocket.request_headers or {}))

                    # put result to response queue
                    await return_response(result, connection_id)
                except Exception as e:
                    LOG.info('Unable to handle incoming websockets message: %s' % e)
                    LOG.debug('Error details: %s %s' % (e, traceback.format_exc()))
        except websockets.exceptions.ConnectionClosedError:
            LOG.info('Connection from WebSocket closed: %s' % websocket)
            # send disconnect message
            if connection_events and not channel_details.get('_disconnected_'):
                message = {'action': '$disconnect'}
                result = await run_sync(message_handler, message=message, connection_id=connection_id,
                    path=path, headers=CaseInsensitiveDict(websocket.request_headers or {}))
                channel_details['_disconnected_'] = True

    async def handle_outgoing(websocket, connection_id):
        q_outgoing = WEBSOCKET_CHANNELS[connection_id]['outgoing']
        while True:
            msg = await receive_from_queue(q_outgoing.sync_q)
            if msg is None:
                continue

            # send result back to websocket
            msg = json.dumps(msg) if isinstance(msg, (dict, list)) else msg
            try:
                await websocket.send(msg)
            except Exception as e:
                LOG.info('Unable to send response to websocket: %s - %s' % (e, msg))

    async def _handle_connection(websocket, path):
        connection_id = short_uid()
        WEBSOCKET_CHANNELS[connection_id] = {
            'outgoing': janus.Queue(),
            'websocket': websocket,
            'event_loop': loop
        }
        asyncio.run_coroutine_threadsafe(handle_outgoing(websocket, connection_id), get_event_loop())
        # send connect message
        if connection_events:
            message = {'action': '$connect'}
            try:
                result = await run_sync(message_handler, message=message, connection_id=connection_id,
                    path=path, headers=CaseInsensitiveDict(websocket.request_headers or {}))
                if isinstance(result, Exception):
                    raise result
            except Exception as e:
                # terminate connection if message handler lambda denies the request
                LOG.debug('Received error on $connect event handler - denying WebSocket connection: %s' % e)
                websocket.close()
                return
        # handle incoming message
        await handle_incoming(websocket, connection_id, path)

    LOG.info('Starting websocket server on port %s' % port)

    async def start_server(shutdown_event):
        serve_func = websockets.serve(_handle_connection, '0.0.0.0', port, loop=loop)
        async with serve_func:
            await shutdown_event.wait()

    shutdown_event = asyncio.Event(loop=loop)
    asyncio.run_coroutine_threadsafe(start_server(shutdown_event), loop)

    class WebSocketStarter(object):
        def stop(self, **kwargs):
            async def set_shutdown_event():
                shutdown_event.set()
            asyncio.run_coroutine_threadsafe(set_shutdown_event(), loop)

    result = WebSocketStarter()
    result.port = port
    TMP_THREADS.append(result)
    # wait until server is up and running
    wait_for_port_open(port)
    return result


def get_event_loop():
    return get_named_event_loop('_websockets_')


def put_outgoing_message(connection_id, message):
    async def put(connection_id, message):
        q_outgoing = WEBSOCKET_CHANNELS[connection_id]['outgoing']
        await q_outgoing.async_q.put(message)

    loop = get_event_loop()
    asyncio.run_coroutine_threadsafe(put(connection_id, message), loop)
