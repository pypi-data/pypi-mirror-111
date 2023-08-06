import os
import time
import json
import sys
import select

from uuid import uuid4
from pathlib import Path
from dvenv.broker import RedisBroker
from dvenv.transact import Request, Commands, RequestError
from dvenv import log

DVENV_CHANNEL_PATH = "./.dvenv/channel"
CARRIAGE_RETURN = "\r\n"
TIMEOUT = 0.001


class Client:
    def __init__(self, *, cfg) -> None:
        self.cfg = cfg
        self.broker = RedisBroker(
            host=cfg["broker_host"],
            port=cfg["broker_port"],
            request_timeout=cfg["request_timeout"],
            response_timeout=cfg["response_timeout"],
        )

        self.environment_path = cfg["environment_path"]
        self.client_id = str(uuid4())
        self.channel_id = self._get_channel_id()
        self.broker.subscribe(self.channel_id)

        self.token = "user1"
        self.msg_backlog = []

    def _get_channel_id(self):
        if os.path.exists(DVENV_CHANNEL_PATH):
            with open(DVENV_CHANNEL_PATH, "r") as f:
                return f.read()
        else:
            return str(uuid4())

    def initialize_channel(self):
        req = Request(
            cmd_id=Commands.INIT,
            data={
                "token": self.token,
                "client_id": self.client_id,
                "channel_id": self.channel_id,
            },
        )
        self.broker.send_request(req)

        response = self._wait_for_response(
            cmd_id=Commands.INIT, timeout=self.cfg["response_timeout"]
        )

        if response is None:
            log.die("No response received from broker")

        response_data = response.get("data")
        if response_data == {}:
            log.action("INIT request accepted")
        elif response_data.get("error") == RequestError.NO_AVAILABILITY:
            log.die("INIT request rejected: server is at capacity")

        Path(".dvenv").mkdir(parents=True, exist_ok=True)
        with open(DVENV_CHANNEL_PATH, "w") as f:
            f.write(self.channel_id)

    def create_new_environment(
        self,
        *,
        python_version,
        path,
    ):
        req = Request(
            cmd_id=Commands.CREATE_ENV,
            data={
                "token": self.token,
                "client_id": self.client_id,
                "channel_id": self.channel_id,
                "python_version": python_version,
                "path": path,
            },
        )
        self.broker.send_message(req, topic=self.channel_id)
        return self.enter_interactive_process()

    def run_python(self):
        req = Request(
            cmd_id=Commands.RUN,
            data={
                "run": ["python", "-i"],
                "token": self.token,
                "client_id": self.client_id,
                "channel_id": self.channel_id,
            },
        )
        self.broker.send_message(req, topic=self.channel_id)
        return self.enter_interactive_process()

    def receive_messages(self):
        response_messages = self.broker.get_messages()

        if len(response_messages) > 0:
            for message in response_messages:
                try:
                    _ = self._parse_channel_message(message["data"].decode())
                except AttributeError:
                    pass

                response_messages = self.broker.get_messages()

    def enter_interactive_process(self):
        process_running = True
        return_code = None

        while process_running:
            self._get_input()

            response_messages = self.broker.get_messages()
            if len(response_messages) > 0:
                for message in response_messages:
                    try:
                        msg = self._parse_channel_message(message["data"].decode())

                        cmd_id = msg.get("cmd_id")
                        if cmd_id is not None and cmd_id == Commands.PROCESS_OUTPUT:
                            self._flush_output(msg)
                        elif cmd_id is not None and cmd_id == Commands.PROCESS_EXIT:
                            return_code = msg["data"]["return_code"]
                            log.action(
                                f"Process exited with return code: {return_code}"
                            )
                            process_running = False
                        elif cmd_id is not None and cmd_id == Commands.CREATE_ENV:
                            pass
                        else:
                            self.msg_backlog.append(self.msg_backlog)
                    except AttributeError:
                        pass

        return return_code

    def _get_input(self):
        input, _, _ = select.select([sys.stdin], [], [], TIMEOUT)

        if input:
            line = sys.stdin.readline().rstrip() + CARRIAGE_RETURN

            req = Request(
                cmd_id=Commands.PROCESS_INPUT,
                data={
                    "token": self.token,
                    "client_id": self.client_id,
                    "channel_id": self.channel_id,
                    "input": line,
                },
            )
            self.broker.send_message(req, topic=self.channel_id)

    def _flush_output(self, msg):
        sys.stdout.write(msg["data"]["output"])
        sys.stdout.flush()

    def _wait_for_response(self, *, cmd_id, timeout):
        start_time = time.time()
        elapsed = 0.0

        while elapsed < timeout:
            response_messages = self.broker.get_messages()

            if len(response_messages) > 0:
                for message in response_messages:
                    try:
                        msg = self._parse_channel_message(message["data"].decode())
                        cmd_id = msg.get("cmd_id")
                        if cmd_id is not None and cmd_id == cmd_id:
                            return msg
                        else:
                            self.msg_backlog.append(self.msg_backlog)
                    except AttributeError:
                        pass

            elapsed = time.time() - start_time

    def _parse_channel_message(self, msg):
        msg = json.loads(msg)
        msg_data = msg["data"]

        client_id = msg_data.get("client_id")
        if client_id is not None:
            return

        return msg
