"""
    domonic.utils
    ====================================
    snippets etc
"""
import typing
import random
from re import sub
from itertools import chain, islice
from collections import Counter


class Utils(object):
    """ utils """

    @staticmethod
    def case_camel(s: str):
        """ case_camel('camel-case') > 'camelCase' """
        s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
        return s[0].lower() + s[1:]

    @staticmethod
    def case_snake(s: str):
        """
        snake('camelCase') # 'camel_case'
        """
        return '_'.join(
            sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
            s.replace('-', ' '))).split()).lower()

    @staticmethod
    def case_kebab(s: str):
        """
        kebab('camelCase') # 'camel-case'
        """
        return '-'.join(
            sub(r"(\s|_|-)+", " ",
            sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
            lambda mo: ' ' + mo.group(0).lower(), s)).split())

    @staticmethod
    def squash(the_list):
        """ turns a 2d array into a flat one """
        return [inner for outer in the_list for inner in outer]

    @staticmethod
    def chunk(list, size):
        """ chunk a list into batches """
        return [list[i:i + size] for i in range(0, len(list), size)]

    @staticmethod
    def dictify(arr):
        """ turns a list into a dictionary where the list items are the keys """
        return dict().fromkeys(arr, 0)

    @staticmethod
    def is_empty(some_str):
        return (not some_str.strip())

    @staticmethod
    def unique(some_arr):
        return list(set(some_arr))

    @staticmethod
    def chunks(iterable, size, format=iter):
        """ Iterate over any iterable (list, set, file, stream, strings, whatever), of ANY size """
        it = iter(iterable)
        while True:
            yield format(chain((it.next(),), islice(it, size - 1)))
    # >>> l = ["a", "b", "c", "d", "e", "f", "g"]
    # >>> for chunk in chunks(l, 3, tuple):
    # ...         print chunk

    @staticmethod
    def clean(lst):
        """ removes falsy values (False, None, 0 and “”) from a list """
        return list(filter(None, lst))

    @staticmethod
    def get_vowels(string):
        return [each for each in string if each in 'aeiou']

    @staticmethod
    def untitle(str):
        """ fooBar """
        return str[:1].lower() + str[1:]

    @staticmethod
    def merge_dictionaries(a, b):
        return {**a, **b}

    @staticmethod
    def to_dictionary(keys, values):
        return dict(zip(keys, values))

    @staticmethod
    def most_frequent(list):
        return max(set(list), key=list.count)

    @staticmethod
    def anagram(first, second):
        return Counter(first) == Counter(second)

    @staticmethod
    def frequency(data):
        freq = {}
        for elem in data:
            if elem in freq:
                freq[elem] += 1
            else:
                freq[elem] = 1
        return freq

    @staticmethod
    def init_assets(dir='assets'):
        from domonic.terminal import mkdir, touch
        mkdir(f"{dir}")
        mkdir(f"{dir}/js")
        mkdir(f"{dir}/css")
        mkdir(f"{dir}/img")
        touch(f"{dir}/js/master.js")
        touch(f"{dir}/css/style.css")
        return

    @staticmethod
    def url2file(url):
        """
        gen a safe filename from a url
        """
        import urllib
        url = "_".join(url.split("/"))
        url = "__".join(url.split(":"))
        filename = urllib.parse.quote_plus(url, '')
        return filename

    @staticmethod
    def permutations(word):
        from itertools import permutations
        return [''.join(perm) for perm in list(permutations(word))]

    @staticmethod
    def random_color(self):
        ''' TODO - remove in 0.3 as we have color class. '''
        r = lambda: random.randint(0, 255)
        return str('#%02X%02X%02X' % (r(), r(), r()))

    @staticmethod
    def escape(s):
        chars = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;"
        }
        return "".join(chars.get(c, c) for c in s)

    @staticmethod
    def unescape(s):
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        s = s.replace("&quot;", '"')
        s = s.replace("&apos;", "'")
        s = s.replace("&amp;", "&")
        return s

    @staticmethod
    def replace_between(content, match, replacement, start=0, end=0):
        front = content[0:start]
        mid = content[start:end]
        end = content[end:len(content)]
        mid = mid.replace(match, replacement)
        return front + mid + end

    @staticmethod
    def truncate(text='', length=0):
        if len(text) > length:
            return text[0:length] + "..."
        else:
            return text + "..."

    # def any_iter(arr):
    #     ''' given a list. returns random until expired '''
    #     random.shuffle(arr)
    #     return (x for x in arr)

    # @staticmethod
    # def unless(value, condition):
        # return value if condition else not value
        # if any(pred(x.item) for x in sequence):

    # TODO -
    # def beautfiy(): # make nice
    # def uglify(): # make not nice
    # def simplify(sentence): # reduce a sentence to its meaning. remove uneeded words.
    # def factualise():  # returns json document of modelled info from general text
