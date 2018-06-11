"""
NLU_LOG_LEVEL=debug python3 -m nlu.utils.data_loader
"""


import os
import yaml
from nlu.log import LOG

def load_nlu_data(data_dir):
    """读取NLU数据目录的信息
    目录中应该有intents与entities子目录，分别保存意图和实体信息，为yaml格式
    """
    assert os.path.exists(data_dir), '数据目录“{}”不存在'.format(data_dir)

    paths = []
    for dirname, _, filenames in os.walk(data_dir):
        filenames = [x for x in filenames if x.endswith('.yml')]
        for filename in filenames:
            path = os.path.join(dirname, filename)
            paths.append(path)

    assert paths, '找不到yaml数据文件，注意要以“.yml”后缀名结尾'

    entities = []
    intents = []

    for path in paths:
        with open(path, 'r') as fp:
            try:
                objs = yaml.load(fp)
            except:
                raise Exception('数据读取错误，可能不是合法YAML文件 “{}”'.format(path))
            assert isinstance(objs, (list, tuple)), \
                '数据文件必须是list or tuple “{}”'.format(path)

            for obj in objs:
                if isinstance(obj, dict):
                    if 'intent' in obj:
                        assert 'data' in obj, '意图必须包括“data”属性 “{}”'.format(path)
                        assert isinstance(obj['data'], (list, tuple)) \
                            and obj['data'], \
                                '意图必须包括“data”且长度大于0 “{}”'.format(path)
                        intents.append(obj)
                    elif 'entity' in obj:
                        assert 'data' in obj, \
                            '实体必须包括“data”属性 “{}”'.format(path)
                        assert isinstance(obj['data'], (list, tuple)) \
                            and obj['data'], \
                                '实体必须包括“data”且长度大于0 “{}”'.format(path)
                        entities.append(obj)

    LOG.debug(
        '读取到了 %s 个intent， %s 个entity',
        len(intents),
        len(entities))

    return intents, entities

def unit_test():
    """unit test"""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(current_dir, '..', '..', 'nlu_data')
    load_nlu_data(data_dir)


if __name__ == '__main__':
    unit_test()
