import sys


class ArgsUtil:
    @staticmethod
    def get_argv(__key__):
        for i in range(len(sys.argv) - 1):
            if sys.argv[i] == __key__:
                return sys.argv[i + 1]
        return ''

    @staticmethod
    def exists(__key__):
        for v in sys.argv:
            if v == __key__:
                return True
        return False
