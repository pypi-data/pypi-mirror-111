from .deathbycaptcha import HttpClient, AccessDeniedException
import traceback
import json
from typing import Optional


def resolver_captcha_tipo1(imagem: str,
                           username: Optional[str] = None,
                           password: Optional[str] = None,
                           token: Optional[str] = None,
                           timeout: Optional[int] = 30):
    result = {
        "text": "",
        "status": False,
        "msg": ""
    }
    try:
        client = HttpClient(username,
                            password,
                            token)

        balance = client.get_balance()
        print(balance)
        captcha = client.decode(imagem, timeout)

        if captcha.get('is_correct') and captcha.get("text"):
            result["text"] = captcha.get("text")
            result["status"] = True
            return result
        else:
            result["msg"] = "Não foi possível realizar o captcha."
            return result
    except Exception as e:
        result["msg"] = str(e)


def resolver_captcha_tipo4(sitekey: str, pageurl: str, username: Optional[str] = None, password: Optional[str] = None, token: Optional[str] = None):
    captcha_dict = {
        "googlekey": sitekey,
        "pageurl": pageurl
    }
    json_Captcha = json.dumps(captcha_dict)

    resultado = None
    client = HttpClient(username, password, token)
    try:
        balance = client.get_balance()
        print(balance)

        captcha = client.decode(type=4, token_params=json_Captcha)
        if captcha:
            # The CAPTCHA was solved; captcha["captcha"] item holds its
            # numeric ID, and captcha["text"] item its a text token".
            print("CAPTCHA %s solved: %s" %
                  (captcha["captcha"], captcha["text"]))
            resultado = captcha["text"]
            if '':  # check if the CAPTCHA was incorrectly solved
                client.report(captcha["captcha"])
                resultado = None
    except AccessDeniedException:
        # Access to DBC API denied, check your credentials and/or balance
        print("error: Access to DBC API denied, check your credentials and/or balance")

    else:
        return resultado


def resolver_captcha_tipo5(key: str, pageurl: str, action: str, username: Optional[str] = None, password: Optional[str] = None, token: Optional[str] = None):

    captcha_dict = {
        'proxy': '',
        'proxytype': '',
        'googlekey': key,
        "pageurl": pageurl,
        'action': action,
        'min_score': "0.3"}

    # Create a json string
    json_captcha = json.dumps(captcha_dict)
    controle = 0
    texto = None
    while texto == None or texto == "%3F":

        #client = SocketClient(username, password, token)
        # to use http client client = HttpClient(username, password)
        client = HttpClient(username, password, token)

        try:
            balance = client.get_balance()
            print(balance)

            # Put your CAPTCHA type and Json payload here:
            captcha = client.decode(type=5, token_params=json_captcha)

            if captcha:
                # The CAPTCHA was solved; captcha["captcha"] item holds its
                # numeric ID, and captcha["text"] item its list of "coordinates".
                #print ("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))

                if '':  # check if the CAPTCHA was incorrectly solved
                    client.report(captcha["captcha"])
        except AccessDeniedException:
            # Access to DBC API denied, check your credentials and/or balance
            print("error: Access to DBC API denied," +
                  "check your credentials and/or balance")

        try:
            texto = captcha["text"]
        except:
            if (controle > 10):
                return False

            pass

        controle += 1

    return texto
