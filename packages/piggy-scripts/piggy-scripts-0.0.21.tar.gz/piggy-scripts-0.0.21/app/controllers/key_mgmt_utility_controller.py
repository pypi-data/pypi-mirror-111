import app.scripts.terminal_scripts as term
import app.scripts.key_mgmt_utility_scripts as kmu
import time
import json


def genECCKeyPair(eni_ip, username, password, key_label):
    resp = _can_connect_to_key_mgmt_utility(eni_ip=eni_ip)
    if resp is True:
        key_handles = kmu.generate_key_pair(
            username=username, password=password, key_label=key_label)
        time.sleep(1)

        pub_key_handle = key_handles['public_key']
        pub_key_pem_file_name = kmu.export_public_key(
            username=username, password=password, pub_key_handle=pub_key_handle)

        with open(pub_key_pem_file_name, 'r') as file:
            pub_key_pem = file.read()

        return json.dumps({
            'data':
                {
                    'label': key_label,
                    'pem': pub_key_pem,
                    'handle': key_handles['public_key'],
                    'private_key_handle': key_handles['private_key']
                },
            'status_code': 200
        })
    else:
        raise ConnectionError(
            f'Unable to connect to the Key Mgmt Utility: {resp}')


def sign(eni_ip, username, password, tx_file, pub_key_handle, private_key_handle, count):
    resp = _can_connect_to_key_mgmt_utility(eni_ip=eni_ip)
    if resp is True:
        signed_tx_file = kmu.sign(
            username=username,
            password=password,
            tx_file=tx_file,
            pub_key_handle=pub_key_handle,
            private_key_handle=private_key_handle,
            count=count
        )
        return signed_tx_file
    else:
        raise ConnectionError(
            f'Unable to connect to the Key Mgmt Utility: {resp}')


def _can_connect_to_key_mgmt_utility(eni_ip):
    configured = term.configure_cloudhsm_client(eni_ip=eni_ip)
    if configured is False:
        raise CloudHSMClientConfigureError(
            'Unable to configure the CloudHSM Client')

    started = term.start_cloudhsm_client()
    if started is False:
        raise CloudHSMClientStartError('Unable to start the ClientHSM Client')

    connected = kmu.test_connection()
    if connected is False:
        raise CloudHSMClientConnectionError(
            'Unable to connect to the CloudHSM Client')

    return True


class CloudHSMClientConnectionError(Exception):
    pass


class CloudHSMClientStartError(Exception):
    pass


class CloudHSMClientConfigureError(Exception):
    pass
