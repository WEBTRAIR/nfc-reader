import binascii
import time
import timeout_decorator
import nfc

def read(timeout_sec):
    started = time.time()
    
    @timeout_decorator.timeout(timeout_sec)
    def on():
        clf = nfc.ContactlessFrontend("usb")
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        clf.close()
        return tag
    
    tag = None
    try:
        tag = on()
    except timeout_decorator.TimeoutError:
        pass

    idm = None
    if tag:
        # attributeerror occurs if the tag does not have an idm.
        # idmがない場合「tag.idm」でAttributeErrorが発生する。
        try:
            idm = binascii.hexlify(tag.idm).decode()
        except AttributeError:
            pass
    # print
    print('tag  : {}'.format(tag))
    print('idm  : {}'.format(idm))
    print('time : {}'.format(time.time()-started))
    return tag,idm