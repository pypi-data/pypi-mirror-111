import re
from io import StringIO

import pandas as pd

from ..checkpoint import CheckpointOpts, CsvContentSerializer
from ..tagged_frame import TaggedFrame

COLON_NUMBER_PATTERN = re.compile(r'\:\d+$')


def to_lemma_form(token: str, baseform: str) -> str:
    lemma = token if baseform.strip('|') == '' else baseform.strip('|').split('|')[0]
    lemma = lemma.replace(' ', '_')
    lemma = COLON_NUMBER_PATTERN.sub('', lemma)
    return lemma


class SparvCsvSerializer(CsvContentSerializer):
    def deserialize(self, content: str, options: CheckpointOpts) -> TaggedFrame:
        """Extracts first part of baseform (format of baseform is `|lemma|xyz|`"""
        df: TaggedFrame = pd.read_csv(
            StringIO(content),
            sep=options.sep,
            quoting=options.quoting,
            index_col=False,
            skiprows=[1],  # XML <text> tag
        ).fillna('')

        df['baseform'] = df.apply(lambda x: to_lemma_form(x['token'], x['baseform']), axis=1)

        return df
