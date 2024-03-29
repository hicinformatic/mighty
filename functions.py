from django.utils.six.moves import input
from django.apps import apps
from mighty.apps import MightyConfig
from django.db.models import F, Func
from Crypto import Cipher, Random
import base64, datetime, string, random, unicodedata, re

BS = MightyConfig.Crypto.BS
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]
numeric_const_pattern = '[-+]? (?: (?: \d* [\.,] \d+ ) | (?: \d+ [\.,]? ) )(?: [Ee] [+-]? \d+ ) ?'

class Round(Func):
  function = 'ROUND'
  arity = 2

def test(input_str=None, search=MightyConfig.Test.search):
    return True if str(input_str).strip().lower().replace(' ', '') not in search else False

def get_or_none(data):
    return data if not test(data) else None

def key(size=32):
    return ''.join(random.choice(string.hexdigits) for x in range(size))

def randomcode(stringLength):
    letters = "123456789"
    return ''.join(random.choice(letters).upper() for i in range(stringLength))

def make_float(flt):
    if test(flt):
        flt = re.compile(numeric_const_pattern, re.VERBOSE).search(flt).group().replace(',', '.')
        return float(flt)
    return None

def make_int(itg):
    if test(itg):
        return int(make_float(itg))
    return None

def make_string(input_str):
    if (',' in input_str):
        input_str = re.sub(r'[^\w\s]',' ',input_str).strip()
        return input_str
    return re.sub(r'[^\w\s]',' ', input_str).strip()

def split_comment(input_str):
    return re.search( "([\w\d&,\. ]+)?\((.*)\)" , input_str)

def encrypt(key, raw):
    raw = pad(raw)
    iv = Random.new().read(Cipher.AES.block_size)
    cipher = Cipher.AES.new(key, Cipher.AES.MODE_CFB, iv)
    return base64.b64encode(iv+cipher.encrypt(raw)) 

def decrypt(key, enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = Cipher.AES.new(key, Cipher.AES.MODE_CFB, iv)
    return unpad(cipher.decrypt(enc[16:]))

def get_model(label, model):
    return apps.get_model(label, model)

def input_get_model(reference):
    label = input("What label is for the reference %s: " % reference)
    model = input("What model is for the reference %s: " % reference)
    return get_model(label, model)

def boolean_input(question, default='n'):
    result = input("%s " % question)
    while len(result) < 1 or result[0].lower() not in "yn":
        result = input("Please answer yes(y) or no(n), default(%s): " % default)
    return result[0].lower() == 'y'

def boolean_input(question, default='n'):
    result = input("%s " % question)
    while len(result) < 1 or result[0].lower() not in "yn":
        result = input("Please answer yes(y) or no(n), default(%s): " % default)
    return result[0].lower() == 'y'

def object_search(model, reference):
    result = input("Make a search that refers to %s (keep empty for pass): " % reference)
    if test(result):
        print(model)
        objects_list = model.objects.filter(to_search__contains=make_searchable(result))
        return multipleobjects_onechoice(objects_list, reference, model)
    return None

def multipleobjects_onechoice(objects_list, reference, model):
    objects = [None, ]
    i = 0
    print("0. for search")
    for obj in objects_list:
        i += 1
        objects.append(obj)
        print("%s. %s" % (i, str(obj)))
    result = input("choose the object that refers to %s (keep empty for pass): " % reference)
    if test(result):
        choice = make_int(result)
        if choice == 0:
            return object_search(model, reference)
        else:
            return objects[choice]
    return None

def foreignkey_from(model, field, data, ret):
    return getattr(model.objects.get(**{field: data}), ret)
    
def make_searchable(input_str):
    for i in MightyConfig.Test.replace:
        input_str = input_str.replace(i, ' ')
    input_str = re.sub(" +", " ", input_str)
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

def image_directory_path(instance, filename):
    directory = str(instance.__class__.__name__).lower()
    date = datetime.datetime.now()
    ext = filename.split('.')[-1:]
    if hasattr(instance, 'uid'):
        return "{0}/{1}/{2}/{3}.{4}".format(directory, date.year, date.month, instance.uid, ext)
    else:
        return "{0}/{1}/{2}/{3}.{4}".format(directory, date.year, date.month, instance.id, ext)

def file_directory_path(instance, filename):
    directory = str(instance.__class__.__name__).lower()
    date = datetime.datetime.now()
    ext = filename.split('.')[-1:]
    if hasattr(instance.parent, 'uid'):
        return "{0}/{1}/{2}/{3}/{4}".format(directory, date.year, date.month, instance.parent.uid, filename)
    else:
        return "{0}/{1}/{2}/{3}/{4}".format(directory, date.year, date.month, instance.parent.id, filename)

def similar_str(str1, str2):
    max_len = tmp = pos1 = pos2 = 0
    len1, len2 = len(str1), len(str2)
    for p in range(len1):
        for q in range(len2):
            tmp = 0
            while p + tmp < len1 and q + tmp < len2 \
                    and str1[p + tmp] == str2[q + tmp]:
                tmp += 1
            if tmp > max_len:
                max_len, pos1, pos2 = tmp, p, q
    return max_len, pos1, pos2

def similar_char(str1, str2):
    max_len, pos1, pos2 = similar_str(str1, str2)
    total = max_len
    if max_len != 0:
        if pos1 and pos2:
            total += similar_char(str1[:pos1], str2[:pos2])
        if pos1 + max_len < len(str1) and pos2 + max_len < len(str2):
            total += similar_char(str1[pos1 + max_len:], str2[pos2 + max_len:]);
    return total

def similar_text(str1, str2):
    if not (isinstance(str1, str) or isinstance(str1, unicode)):
        raise TypeError("must be str or unicode")
    elif not (isinstance(str2, str) or isinstance(str2, unicode)):
        raise TypeError("must be str or unicode")
    elif len(str1) == 0 and len(str2) == 0:
        return 0.0
    else:
        return int(similar_char(str1, str2) * 200.0 / (len(str1) + len(str2)))

#0 	Emergency 	  emerg (panic)	 Système inutilisable.
#1 	Alert 	      alert          Une intervention immédiate est nécessaire.
#2 	Critical 	  crit 	         Erreur critique pour le système.
#3 	Error 	      err (error) 	 Erreur de fonctionnement.
#4 	Warning 	  warn (warning) Avertissement (une erreur peut intervenir si aucune action n'est prise).
#5 	Notice 	      notice  	     Evénement normal méritant d'être signalé.
#6 	Informational info 	         Pour information.
#7 	Debugging 	  debug 	     Message de mise au point.
def logger(app, lvl, msg, user=None):
    code = getattr(MightyConfig.Log, MightyConfig.Log.format_code.format(lvl))
    if code <= MightyConfig.Log.log_level:
        if user is not None:
            msg = MightyConfig.Log.format_user.format(user.username, user.id, msg)
        if MightyConfig.Log.log_type == 'syslog':
            logger_syslog(app, lvl, code, msg)
        elif MightyConfig.Log.log_type == 'file':
            logger_file(app, lvl, code, msg)
        else:
            logger_console(app, lvl, code, msg)

def logger_syslog(app, lvl, code, msg):
    syslog.openlog(logoption=syslog.LOG_PID)
    syslog.syslog(code, MightyConfig.Log.format_syslog.format(app, msg))
    syslog.closelog()

def logger_file(app, lvl, code, msg):
    now = datetime.datetime.now()
    logfile = MightyConfig.Log.name_file.format(MightyConfig.Directory.logs, app, now.year, now.month, now.day)
    log = open(logfile, MightyConfig.Log.file_open_method)
    log.write(MightyConfig.Log.format_file.format(now.hour, now.minute, now.second, now.microsecond, lvl, app, msg))
    log.close()

def logger_console(app, lvl, code, msg):
    color = getattr(MightyConfig.Log, MightyConfig.Log.format_color.format(lvl))
    now = datetime.datetime.now()
    print(MightyConfig.Log.format_console.format(color, now.hour, now.minute, now.second, now.microsecond, lvl, app, msg, MightyConfig.Log.default_color))