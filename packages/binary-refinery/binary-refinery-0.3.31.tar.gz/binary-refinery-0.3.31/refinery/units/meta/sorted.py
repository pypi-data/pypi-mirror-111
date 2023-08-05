#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .. import arg, Unit, RefineryCriticalException
from ...lib.argformats import PythonExpression


class sorted(Unit):
    """
    Sorts all elements of the input `refinery.lib.frame` lexicographically.
    This unit is a `refinery.nop` on single inputs.
    """

    def __init__(
        self,
        key: arg('key', type=str, help='A meta variable expression to sort by instead of sorting the content.') = None,
        length: arg.switch('-l', help='Sort items by length before sorting lexicographically.') = False
    ):
        super().__init__(key=key, length=length)

    def filter(self, chunks):
        sortbuffer = []
        invisibles = {}

        if self.args.key is None:
            if self.args.length:
                def key(chunk):
                    return (len(chunk), chunk)
            else:
                key = None
        else:
            expression = PythonExpression(self.args.key, all_variables_allowed=True)
            if self.args.length:
                def key(chunk):
                    r = expression(**chunk.meta)
                    return (len(r), r)
            else:
                def key(chunk):
                    return expression(**chunk.meta)

        for k, chunk in enumerate(chunks):
            if not chunk.visible:
                r = k - len(invisibles)
                invisibles.setdefault(r, [])
                invisibles[r].append(chunk)
            else:
                sortbuffer.append(chunk)

        sortbuffer.sort(key=key)

        if not invisibles:
            yield from sortbuffer
            return

        for r, chunk in enumerate(sortbuffer):
            if r in invisibles:
                yield from invisibles[r]
                del invisibles[r]
            yield chunk

        if invisibles:
            yield from invisibles[r]
            del invisibles[r]

        if invisibles:
            raise RefineryCriticalException(
                'for unknown reasons, invisible chunks were lost during '
                'the sorting process.'
            )
